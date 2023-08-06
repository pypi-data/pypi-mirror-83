"""
    tiamatpip.cli
    ~~~~~~~~~~~~~

    PIP handling for tiamat packaged python projects
"""
import code
import logging
import os
import pathlib
import sys
from typing import List
from typing import Sequence

from pip._internal.cli.main import main as pip_main
from pip._internal.commands.install import InstallCommand
from pip._internal.commands.uninstall import UninstallCommand

from tiamatpip import configure
from tiamatpip.store import DistributionNotFound
from tiamatpip.store import Store
from tiamatpip.utils import debug_print
from tiamatpip.utils import patch_pip_get_installed_distributions
from tiamatpip.utils import patched_environ
from tiamatpip.utils import patched_sys_argv

# If there are logging handlers already configured, then the basicConfig
# call below will be a no-op
logging.basicConfig(
    stream=sys.stderr,
    format="%(message)s",
    level=logging.DEBUG if "TIAMAT_PIP_DEBUG" in os.environ else logging.INFO,
)
log = logging.getLogger(__name__)


def should_redirect_argv(argv):
    debug_print("should_redirect_argv", argv)
    if "TIAMAT_PIP_INSTALL" in os.environ:
        # A pip command is already in progress. This is usually
        # hit when pip is building the dependencies of a package
        return True
    if argv[1] == configure.get_pip_command_name():
        # We should intercept pip comands
        return True
    # Do nothing
    return False


def process_argv(argv: List[str]) -> bool:
    pypath = configure.get_user_site_packages_path()
    debug_print("process_argv", argv, pypath=pypath, pypath_exists=pypath.exists())
    if "TIAMAT_PIP_INSTALL" not in os.environ:
        log.debug("Not processing argv since TIAMAT_PIP_INSTALL is not in os.environ")
        return False

    cpath = os.environ.get("CPATH") or None
    c_include_path = os.environ.get("C_INCLUDE_PATH") or None

    pyinstaller_extract_path = sys._MEIPASS  # pylint: disable=no-member
    included_python_headers_path = str(
        pathlib.Path(pyinstaller_extract_path).resolve() / "include" / "python"
    )
    if cpath is None:
        cpath = included_python_headers_path
    else:
        cpath_parts = cpath.split(os.pathsep)
        if included_python_headers_path not in cpath_parts:
            cpath_parts.append(included_python_headers_path)
        cpath = os.pathsep.join(cpath_parts)
    if c_include_path is None:
        c_include_path = included_python_headers_path
    else:
        c_include_path_parts = c_include_path.split(os.pathsep)
        if included_python_headers_path not in c_include_path_parts:
            c_include_path_parts.append(included_python_headers_path)
        c_include_path = os.pathsep.join(c_include_path_parts)
    with patched_environ(C_INCLUDE_PATH=c_include_path, CPATH=cpath):
        if argv[1] == "-c":
            # Example:
            #   python -c "print 'Foo!'"
            run_code(argv[2:])
            return
        elif argv[1] == "-u" and argv[2] == "-c":
            # Example:
            #   python -u -c "print 'Foo!'"
            run_code(argv[3:])
            return

        try:
            argv1_file = pathlib.Path(argv[1]).resolve()
            if argv1_file.is_file() and not str(argv1_file).endswith(f"{os.sep}pip"):
                # Example:
                #   python this-is-a-script.py arg1 arg2
                run_python_file(argv[1:])
                return
        except ValueError:
            # Not a valid file
            pass

        if argv[1] == "-m" and argv[2] == "pip":
            # Example:
            #   python -m pip install foo
            argv.pop(1)
        redirect_to_pip(argv)
        return True


def process_pip_argv(argv: List[str]) -> None:
    pypath = configure.get_user_site_packages_path()
    debug_print("process_pip_argv", argv, pypath=pypath, pypath_exists=pypath.exists())
    if pypath is None:
        raise RuntimeError(
            "You need to run 'tiamatpip.configure.set_user_site_packages_path(<path>)' "
            "before calling tiamatpip.cli.process_pip_argv()"
        )

    if not pypath.is_dir():
        log.error(f"The path '{pypath}' does not exist or could not be created.")
        sys.exit(1)

    environ = {
        "TIAMAT_PIP_INSTALL": "1",
        "TIAMAT_PIP_PYPATH": str(pypath),
    }
    with patched_environ(environ=environ):
        return process_argv(argv)


def redirect_to_pip(argv: List[str]) -> None:
    pypath = configure.get_user_site_packages_path()
    debug_print("redirect_to_pip", argv, pypath=pypath, pypath_exists=pypath.exists())
    targets: Sequence[str] = ("install", "list", "freeze", "uninstall")
    try:
        cmd = argv[2]
    except IndexError:
        msg: str = "Must pass in available pip command which are:"
        for cmd in targets:
            msg += f"\n - {cmd}"
        log.error(msg)
        sys.exit(1)

    user_site_path = configure.get_user_site_packages_path()
    extra_environ = {
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        # The environment variable PYTHONUSERBASE can also be used to
        # tell pip where to install packages into
        "PYTHONUSERBASE": str(user_site_path),
    }

    # Valid command found

    if cmd in ("install", "uninstall"):
        include_in_store = True
    else:
        include_in_store = False
    if cmd == "install":
        args = [cmd]
        for arg in argv:
            if arg == "--prefix" or arg.startswith("--prefix="):
                # When pip is building dependencies it might build them in isolation
                # or pass --prefix.
                # We should not inject our --target in this scnario
                log.debug(f"Found '{arg}' in argv. Not adding our own target.")
                # If the package is meant to be installed in our pypath, don't
                # keep track of it in our store
                include_in_store = False
                break
        else:
            # Install into our custom site packages target path
            args.extend(["--target", str(user_site_path)])
    elif cmd == "uninstall":
        args = [cmd]
        patch_pip_get_installed_distributions()
        extra_environ["TIAMAT_PIP_UNINSTALL"] = "1"
    elif cmd in ("list", "freeze"):
        args = [cmd, "--path", str(user_site_path)]
    else:
        args = [cmd]
    args.extend(argv[3:])
    pkgs = []
    if cmd in ("install", "uninstall"):
        if cmd == "install":
            parser = InstallCommand("name", "summary")
        else:
            parser = UninstallCommand("name", "summary")
        _, _args = parser.parse_args(args[:])
        pkgs.extend(_args[1:])
        log.debug(f"Packages to install: {pkgs}")

    # Call pip
    with patched_environ(environ=extra_environ):
        try:
            exitcode = call_pip(args)
            if include_in_store is True:
                store = Store()
                for pkg in pkgs:
                    try:
                        if cmd == "install":
                            store.add(pkg)
                        else:
                            store.remove(pkg)
                    except DistributionNotFound as exc:
                        log.error(str(exc))
                        exitcode = 1
                store.write()
            sys.exit(exitcode)
        finally:
            pypath = configure.get_user_site_packages_path()
            debug_print(
                "redirect_to_pip finally",
                args,
                pypath=pypath,
                pypath_exists=pypath.exists(),
            )


def call_pip(argv):
    debug_print("call_pip", argv)
    return pip_main(argv)


def run_code(argv):
    source, *_ = argv
    with patched_sys_argv(argv):
        debug_print("run_code", argv)
        interpreter = code.InteractiveInterpreter()
        interpreter.runsource(source)


def run_python_file(argv):
    debug_print("run_python_file", argv)
    python_file, *_ = argv
    with open(python_file) as rfh:
        source = rfh.read()
        with patched_sys_argv(argv):
            # We want scripts which have an 'if __name__ == "__main__":'
            # section to run it
            interpreter = code.InteractiveInterpreter({"__name__": "__main__"})
            interpreter.runsource(source, filename=python_file, symbol="exec")
