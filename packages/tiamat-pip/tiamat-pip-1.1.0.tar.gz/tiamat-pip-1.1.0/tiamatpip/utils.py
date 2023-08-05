"""
    tiamat.pip.utils
    ~~~~~~~~~~~~~~~~

    @todo: add description
"""
import logging
import os
import pathlib
import pprint
import sys
from contextlib import contextmanager
from typing import Container
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Sequence

from pip._internal.utils import misc

from tiamatpip import configure

# Hold a reference to the real function
real_get_installed_distributions = misc.get_installed_distributions

DEBUG = "TIAMAT_PIP_DEBUG" in os.environ
log = logging.getLogger(__name__)


@contextmanager
def changed_permissions(path: pathlib.Path, mode: int, skip: bool = False) -> Generator:
    if skip is False:
        previous_mode = path.stat().st_mode
    try:
        if skip is False:
            print("Setting mode {} to {}".format(oct(previous_mode | mode), path))
            for entry in path.rglob("*"):
                entry.chmod(previous_mode | mode)
        yield
    finally:
        if skip is False:
            print("Re-Setting mode {} to {}".format(oct(previous_mode), path))
            for entry in path.rglob("*"):
                entry.chmod(previous_mode)


@contextmanager
def patched_environ(
    *, environ: Optional[Dict[str, str]] = None, **kwargs: str
) -> Generator:
    _environ = environ.copy() if environ else {}
    _environ.update(**kwargs)
    old_values = {}
    try:
        for key, value in _environ.items():
            msg_prefix = "Setting"
            if key in os.environ:
                msg_prefix = "Updating"
                old_values[key] = os.environ[key]
            log.debug(f"{msg_prefix} environ variable {key} to: '{value}'")
            os.environ[key] = value
        yield
    finally:
        for key in _environ:
            if key in old_values:
                log.debug(f"Restoring environ variable {key} to: '{old_values[key]}'")
                os.environ[key] = old_values[key]
            else:
                if key in os.environ:
                    log.debug(f"Removing environ variable {key}")
                    os.environ.pop(key)


@contextmanager
def patched_sys_argv(argv: Sequence[str]) -> Generator:
    previous_sys_argv = list(sys.argv)
    try:
        log.debug(f"Patching sys.argv to: {argv}")
        sys.argv[:] = argv
        yield
    finally:
        log.debug(f"Restoring sys.argv to: {previous_sys_argv}")
        sys.argv[:] = previous_sys_argv


def get_installed_distributions(
    local_only: bool = True,
    skip: Container[str] = misc.stdlib_pkgs,
    include_editables: bool = True,
    editables_only: bool = False,
    user_only: bool = False,
    paths: Optional[List[pathlib.Path]] = None,
):
    if "TIAMAT_PIP_UNINSTALL" in os.environ:
        if paths is None:
            paths = []
        pypath = configure.get_user_site_packages_path()
        if pypath:
            paths.append(pypath)
    return real_get_installed_distributions(
        local_only=local_only,
        skip=skip,
        include_editables=include_editables,
        editables_only=editables_only,
        user_only=user_only,
        paths=paths,
    )


def patch_pip_get_installed_distributions():
    misc.get_installed_distributions = get_installed_distributions


def debug_print(funcname: str, argv: List[str], **extra: str) -> None:
    if DEBUG is False:
        return
    prefixes_of_interest = ("TIAMAT_", "LD_", "C_", "CPATH")
    environ = {}
    for key, value in os.environ.items():
        if key.startswith(prefixes_of_interest):
            environ[key] = value
    header = f"Func: {funcname}"
    tail_len = 70 - len(header) - 5
    print(f">>> {header} " + ">" * tail_len, file=sys.stderr, flush=True)
    print(f"  CWD: {os.getcwd()}", file=sys.stderr, flush=True)
    print(f"  ENVIRON:\n{pprint.pformat(environ)}", file=sys.stderr, flush=True)
    print(f"  ARGV:\n{pprint.pformat(argv)}", file=sys.stderr, flush=True)
    if extra:
        print("  EXTRA:", file=sys.stderr, flush=True)
    for key, value in extra.items():
        print(f"    {key}: {value}", file=sys.stderr, flush=True)
    print(f"<<< {header} " + "<" * tail_len, file=sys.stderr, flush=True)
