from __future__ import print_function

import enum
import logging
import os
import platform
import struct
import sys
import sysconfig
from typing import Iterable, Optional, Sequence, Tuple

import pkg_resources
import six

import req_compile.errors
import req_compile.utils
from req_compile.containers import DistInfo
from req_compile.errors import NoCandidateException
from req_compile.filename import parse_source_filename
from req_compile.utils import have_compatible_glibc, normalize_project_name

INTERPRETER_TAGS = {
    "CPython": "cp",
    "IronPython": "ip",
    "PyPy": "pp",
    "Jython": "jy",
}

INTERPRETER_TAG = INTERPRETER_TAGS.get(platform.python_implementation(), "cp")
PY_VERSION_NUM = str(sys.version_info.major) + str(sys.version_info.minor)


def is_manylinux2010_compatible():
    # type: () -> bool
    # Check for presence of _manylinux module
    try:
        import _manylinux  # type: ignore  # pylint: disable=bad-option-value,import-outside-toplevel

        return bool(_manylinux.manylinux2010_compatible)
    except (ImportError, AttributeError):
        # Fall through to heuristic check below
        pass

    # Check glibc version. CentOS 6 uses glibc 2.12.
    # PEP 513 contains an implementation of this function.
    return have_compatible_glibc(2, 12)


def is_manylinux2014_compatible():
    # type: () -> bool
    # Only Linux, and only supported architectures
    if platform.machine() not in (
        "x86_64",
        "i686",
        "aarch64",
        "armv7l",
        "ppc64",
        "ppc64le",
        "s390x",
    ):
        return False

    # Check for presence of _manylinux module
    try:
        import _manylinux  # pylint: disable=bad-option-value,import-outside-toplevel

        return bool(_manylinux.manylinux2014_compatible)
    except (ImportError, AttributeError):
        # Fall through to heuristic check below
        pass

    # Check glibc version. CentOS 7 uses glibc 2.17.
    # PEP 513 contains an implementation of this function.
    return have_compatible_glibc(2, 17)


def _get_platform_tags():
    # type: () -> Sequence[str]
    is_32 = struct.calcsize("P") == 4
    if sys.platform == "win32":
        if is_32:
            tag = ("win32",)
        else:
            tag = ("win_amd64",)
    elif sys.platform.startswith("linux"):
        if is_32:
            arch_tag = platform.machine()
        else:
            arch_tag = "x86_64"

        tag = (
            ("linux_" + arch_tag),
            ("manylinux1_" + arch_tag),
        )
        if is_manylinux2010_compatible():
            tag += ("manylinux2010_" + arch_tag,)
        if is_manylinux2014_compatible():
            tag += ("manylinux2014_" + arch_tag,)
    else:
        raise ValueError("Unsupported platform: {}".format(sys.platform))
    return ("any",) + tag


def _get_abi_tag():
    # type: () -> str
    """Build a best effort ABI tag"""
    py_version = (sys.version_info.major, sys.version_info.minor)
    tag = INTERPRETER_TAG + PY_VERSION_NUM
    if py_version < (3, 8):
        pymalloc = sysconfig.get_config_var("WITH_PYMALLOC")
        if pymalloc or pymalloc is None:
            tag += "m"
        if py_version < (3, 3):
            unicode_size = sysconfig.get_config_var("Py_UNICODE_SIZE")
            if unicode_size == 4 or (
                unicode_size is None and sys.maxunicode == 0x10FFFF
            ):
                tag += "u"
    return tag


PLATFORM_TAGS = _get_platform_tags()
ABI_TAGS = ("abi" + str(sys.version_info.major), _get_abi_tag())


class RepositoryInitializationError(ValueError):
    """Failure to initialize a repository"""

    def __init__(self, repo_type, message):
        super(RepositoryInitializationError, self).__init__(message)
        self.type = repo_type


class DistributionType(enum.IntEnum):
    SOURCE = 2
    WHEEL = 1
    SDIST = 0


class PythonVersionRequirement(object):
    def check_compatibility(self):
        raise NotImplementedError


def _all_py_tags_in_major(up_to):
    up_to = int(up_to)
    while (up_to % 10) > 0:
        yield INTERPRETER_TAG + str(up_to)
        yield "py" + str(up_to)
        up_to -= 1
    yield "py" + str(up_to)


class WheelVersionTags(PythonVersionRequirement):
    WHEEL_VERSION_TAGS = (
        "py2" if six.PY2 else "py3",
        INTERPRETER_TAG + PY_VERSION_NUM,
    ) + tuple(_all_py_tags_in_major(PY_VERSION_NUM))

    def __init__(self, py_version):
        self.py_version = py_version

    def check_compatibility(self):
        if not self.py_version:
            return True
        return any(
            version in WheelVersionTags.WHEEL_VERSION_TAGS
            for version in self.py_version
        )

    def __str__(self):
        if self.py_version is None or self.py_version == ():
            return "any"

        return ".".join(sorted(self.py_version))

    def __eq__(self, other):
        return self.py_version == other.py_version

    @property
    def tag_score(self):
        result = 100
        version_val = None
        if len(self.py_version) == 1:
            version_val = self.py_version[0]

        if version_val is not None:
            for tag_type in tuple(INTERPRETER_TAGS.values()) + ("py",):
                version_val = version_val.replace(tag_type, "")
            try:
                result += int(version_val)
            except ValueError:
                pass

        return result


class Candidate(object):  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        name,
        filename,
        version,
        py_version,
        abi,
        plat,
        link,
        candidate_type=DistributionType.SDIST,
        extra_sort_info="",
    ):
        """

        Args:
            name:
            filename:
            version:
            py_version (RequiresPython): Python version
            abi (str, None)
            plat (str):
            link:
            candidate_type:
        """
        self.name = name
        self.filename = filename
        self.version = version or pkg_resources.parse_version("0.0.0")
        self.py_version = py_version
        self.abi = abi
        self.platform = plat
        self.link = link
        self.type = candidate_type

        # Sort based on tags to make sure the most specific distributions
        # are matched first
        self._sortkey = None
        self._extra_sort_info = extra_sort_info

        self.preparsed = None

    @property
    def sortkey(self):
        if self._sortkey is None:
            self._sortkey = (
                self.version,
                self._extra_sort_info,
                self.type.value,
                self.tag_score,
            )
        return self._sortkey

    @property
    def tag_score(self):
        py_version_score = (
            self.py_version.tag_score if self.py_version is not None else 0
        )
        try:
            abi_score = ABI_TAGS.index(self.abi) if self.abi is not None else 0
        except ValueError:
            abi_score = 0
        try:
            plat_score = PLATFORM_TAGS.index(self.platform.lower())
        except ValueError:
            plat_score = 0
        # Spaces in source dist filenames penalize them in the search order
        extra_score = (
            0
            if isinstance(self.filename, six.string_types) and " " in self.filename
            else 1
        )
        return py_version_score, plat_score, abi_score, extra_score

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.filename == other.filename
            and self.version == other.version
            and self.py_version == other.py_version
            and self.abi == other.abi
            and self.platform == other.platform
            and self.link == other.link
            and self.type == other.type
        )

    def __repr__(self):
        return "Candidate(name={}, filename={}, version={}, py_version={}, abi={}, platform={}, link={})".format(
            self.name,
            self.filename,
            self.version,
            self.py_version,
            self.abi,
            self.platform,
            self.link,
        )

    def __str__(self):
        py_version_str = str(self.py_version) + "-"
        return "{} {}-{}-{}{}-{}".format(
            self.type.name,
            self.name,
            self.version,
            py_version_str,
            self.abi,
            self.platform,
        )


def process_distribution(source, filename):
    candidate = None
    if filename.endswith(".egg"):
        return None
    if ".whl" in filename:
        candidate = _wheel_candidate(source, filename)
    elif (
        ".tar.gz" in filename
        or ".tgz" in filename
        or ".zip" in filename
        or ".tar.bz2" in filename
    ):
        # Best effort skip of dumb binary distributions
        if ".linux-" in filename or ".win-" in filename or ".macosx-" in filename:
            return None
        candidate = _tar_gz_candidate(source, filename)
    return candidate


def _wheel_candidate(source, filename):
    filename = os.path.basename(filename)
    data_parts = filename.split("-")
    if len(data_parts) < 5:
        logging.getLogger("req_compile.repository").debug(
            "Unable to use %s, improper filename", filename
        )
        return None

    has_build_tag = len(data_parts) == 6
    build_tag = ""
    if has_build_tag:
        build_tag = data_parts.pop(2)
    name = data_parts[0]
    abi = data_parts[3]
    #  Convert old-style post-versions to new style so it will sort correctly
    version = pkg_resources.parse_version(data_parts[1].replace("_", "-"))
    plat = data_parts[4].split(".")[0]

    requires_python = WheelVersionTags(tuple(data_parts[2].split(".")))

    return Candidate(
        name,
        filename,
        version,
        requires_python,
        abi if abi != "none" else None,
        plat,
        source,
        candidate_type=DistributionType.WHEEL,
        extra_sort_info=build_tag,
    )


def _tar_gz_candidate(source, filename):
    name, version = parse_source_filename(os.path.basename(filename))
    return Candidate(
        name,
        filename,
        version,
        None,
        None,
        "any",
        source,
        candidate_type=DistributionType.SDIST,
    )


def _check_platform_compatibility(py_platform):
    return py_platform == "any" or (py_platform.lower() in PLATFORM_TAGS)


def _check_abi_compatibility(abi):
    return abi in ABI_TAGS


class BaseRepository(object):
    def get_candidate(self, req, max_downgrade=None):
        # type: (pkg_resources.Requirement, int) -> Tuple[DistInfo, bool]
        """Fetch the best matching candidate for the given requirement

        Args:
            req: Requirement to find a match for
            max_downgrade: Maximum number of different versions to try if
                metadata parsing fails

        Returns:
            (Candidate) The best matching candidate
        """
        raise NotImplementedError()


class CantUseReason(enum.Enum):
    U_CAN_USE = 0
    WRONG_PYTHON_VERSION = 2
    WRONG_PLATFORM = 3
    IS_PRERELEASE = 4
    VERSION_NO_SATISFY = 5
    BAD_METADATA = 6
    NAME_DOESNT_MATCH = 7
    WRONG_ABI = 8


def sort_candidates(candidates):
    """

    Args:
        candidates:

    Returns:
        (list[Candidate])
    """
    return sorted(candidates, key=lambda x: x.sortkey, reverse=True)


def check_usability(req, candidate, has_equality=None, allow_prereleases=False):
    # type: (pkg_resources.Requirement, Candidate, bool, bool) -> Optional[CantUseReason]
    if (
        candidate.py_version is not None
        and not candidate.py_version.check_compatibility()
    ):
        return CantUseReason.WRONG_PYTHON_VERSION

    if candidate.abi is not None and not _check_abi_compatibility(candidate.abi):
        return CantUseReason.WRONG_ABI

    if not _check_platform_compatibility(candidate.platform):
        return CantUseReason.WRONG_PLATFORM

    if not has_equality and not allow_prereleases and candidate.version.is_prerelease:
        return CantUseReason.IS_PRERELEASE

    if req is not None and not req.specifier.contains(  # type: ignore[attr-defined]
        candidate.version, prereleases=has_equality or allow_prereleases
    ):
        return CantUseReason.VERSION_NO_SATISFY

    return None


def filter_candidates(req, candidates, allow_prereleases=False):
    # type: (pkg_resources.Requirement, Iterable[Candidate], bool) -> Iterable[Candidate]
    has_equality = (
        req_compile.utils.is_pinned_requirement(req) if req is not None else False
    )

    for candidate in candidates:
        if (
            check_usability(
                req,
                candidate,
                has_equality=has_equality,
                allow_prereleases=allow_prereleases,
            )
            is None
        ):
            yield candidate


def _is_all_prereleases(candidates):
    all_prereleases = True
    for candidate in candidates:
        all_prereleases = all_prereleases and candidate.version.is_prerelease
    return all_prereleases


class Repository(BaseRepository):
    def __init__(self, logger_name, allow_prerelease=None):
        # type: (str, bool) -> None
        super(Repository, self).__init__()
        if allow_prerelease is None:
            allow_prerelease = False
        self.logger = logging.getLogger("req_compile.repository").getChild(logger_name)
        self.allow_prerelease = allow_prerelease

    def __eq__(self, other):
        return self.allow_prerelease == other.allow_prerelease

    def __iter__(self):
        return iter([self])

    def get_candidates(self, req):
        """
        Fetch all available candidates for a project_name
        Args:
            req (Requirement): Requirement to get candidates for

        Returns:
            (list[Candidate]) List of candidates
        """
        raise NotImplementedError()

    def resolve_candidate(self, candidate):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def get_candidate(self, req, max_downgrade=None):
        # type: (pkg_resources.Requirement, int) -> Tuple[DistInfo, bool]
        self.logger.info("Getting candidate for %s", req)
        candidates = self.get_candidates(req)
        return self.do_get_candidate(req, candidates, max_downgrade=max_downgrade)

    def do_get_candidate(
        self, req, candidates, force_allow_prerelease=False, max_downgrade=None
    ):
        # type: (pkg_resources.Requirement, Iterable[Candidate], bool, int) -> Tuple[DistInfo, bool]
        """

        Args:
            req: Requirement to fetch candidate for
            candidates: Available candidates (any versions, unsorted)
            force_allow_prerelease: Override the allow prerelease setting
            max_downgrade: Number of different versions to try. Does not limit number of candidates
                per version nor make any judgements about the semver
        Returns:
            The distribution and whether or not it was cached
        """
        allow_prereleases = force_allow_prerelease or self.allow_prerelease
        if candidates:
            filtered_candidates = filter_candidates(
                req, candidates, allow_prereleases=allow_prereleases
            )
            tried_versions = set()

            for candidate in sort_candidates(filtered_candidates):
                if candidate.version is None:
                    self.logger.warning(
                        "Found candidate with no version: %s", candidate
                    )
                    continue

                if candidate.type == DistributionType.SDIST:
                    self.logger.warning(
                        "Considering source distribution for %s", candidate.name
                    )

                try:
                    candidate, cached = self.resolve_candidate(candidate)
                    if candidate is not None:
                        if normalize_project_name(
                            candidate.name
                        ) == normalize_project_name(req.project_name):
                            return candidate, cached
                except req_compile.errors.MetadataError as ex:
                    self.logger.warning(
                        "Could not use candidate %s - %s", candidate, ex
                    )

                tried_versions.add(candidate.version)
                if max_downgrade is not None and len(tried_versions) >= max_downgrade:
                    break

        if (
            _is_all_prereleases(candidates) or req_compile.utils.has_prerelease(req)
        ) and not allow_prereleases:
            self.logger.debug(
                "No non-prerelease candidates available. Now allowing prereleases"
            )
            return self.do_get_candidate(
                req,
                candidates,
                force_allow_prerelease=True,
                max_downgrade=max_downgrade,
            )

        raise NoCandidateException(req)

    def why_cant_I_use(self, req, candidate):  # pylint: disable=invalid-name
        # type: (pkg_resources.Requirement, Candidate) -> CantUseReason
        reason = check_usability(
            req,
            candidate,
            allow_prereleases=self.allow_prerelease,
        )
        if reason is None:
            return CantUseReason.U_CAN_USE
        return reason
