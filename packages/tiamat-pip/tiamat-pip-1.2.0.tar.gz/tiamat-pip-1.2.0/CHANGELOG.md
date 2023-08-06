# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2020.10.22
- Don't use pip's `setup_logging`. This actually added a `StreamHandler` writing to
`sys.stdout` breaking Salt's own logging which only writes to `sys.stderr`.
- Remove unused `tiamatpip.utils.changed_permissions` function.
- Started using `setuptools_scm` for versioning.

## [1.1.1] - 2020-10-21
- When checking installed packages from a `pkg_resources.WorkingSet()` use `.key` not
`.project_name` so that we can match against the canonicalized name.
- Print the `DistributionNotFound` exception message to `sys.stderr` and set exitcode
to 1 instead of printing the traceback.

## [1.1.0] - 2020-10-21
- Added store support to keep track of what's installed/uninstalled. Fixed #2.

## [1.0.0] - 2020-10-13
### Added
- Start keeping a changes log
- Allow showing what the library is doing by adding `TIAMAT_PIP_DEBUG=1` to the environment
- `set_user_site_packages_path` now optionaly creates the path. Set to true by default.
- tiamat-pip will now make sure the python headers are included in the generated binary so
that these are available when `pip install`'ing a package than needs to link to the "embedded"
python interpreter.

## [0.10.0] - 2020-10-09
### Added
- Make sure `pypath` comes first in sys.path

## [0.10.0rc1] - 2020-10-08
### Added
- Stopped changing permissions on the `pypath` directory.
- Error out on missing `pypath` directory

## [0.9.0] - 2020-10-01
### Added
- First working version of the project
