import json
import shutil
import sys
from datetime import datetime

import pkg_resources
from pip._vendor.packaging.utils import canonicalize_name

from tiamatpip import configure


def get_distribution(pkg, pypath):
    pkg = canonicalize_name(pkg)
    working_set = pkg_resources.WorkingSet([pypath])
    for dist in working_set:
        if dist.key == pkg:
            return dist
    raise DistributionNotFound(f"Distribution {pkg} was not found installed")


class DistributionNotFound(Exception):
    pass


class InstalledPackage:
    __slots__ = ("name", "version", "install_date")

    def __init__(self, name, version, install_date=None):
        self.name = name
        self.version = version
        if isinstance(install_date, str):
            install_date = datetime.strptime(install_date, "%Y-%m-%dT%H:%M:%S.%f")
        self.install_date = install_date

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} name={self.name}, "
            f"version={self.version}, "
            f"install_date={self.install_date.isoformat()}>"
        )

    @classmethod
    def from_distribution(cls, distribution):
        return cls(
            distribution.key,
            version=str(distribution.version),
            install_date=datetime.utcnow(),
        )

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "install_date": self.install_date.isoformat(),
        }


class Store:
    fmt_version = 1

    slots = ("_pypath", "_path", "_path_save", "_store", "_py_version", "fmt_version")

    def __init__(self, pypath=None):
        self._store = {}
        self._pypath = pypath = pypath or configure.get_user_site_packages_path()
        self._path = pypath / ".installs.json"
        self._path_save = pypath / ".installs.json.new"
        self._py_version = sys.version_info[:3]
        if self._path.exists():
            try:
                contents = self._path.read_text()
                store = json.loads(contents)
                self._py_version = store["python_version"]
                for entry in store["packages"]:
                    ipkg = InstalledPackage(**entry)
                    self._store[ipkg.name] = ipkg
            except ValueError:
                pass

    def __repr__(self):
        return f"<{self.__class__.__name__} path={self._path}, stored={self._store}>"

    def add(self, pkg):
        distribution = get_distribution(pkg, self._pypath)
        ipkg = InstalledPackage.from_distribution(distribution)
        self._store[ipkg.name] = ipkg

    def remove(self, pkg):
        pkg = canonicalize_name(pkg)
        if pkg in self._store:
            self._store.pop(pkg)
            return
        raise DistributionNotFound(f"The '{pkg}' package was not found installed")

    def write(self):
        data = {
            "fmt_version": self.fmt_version,
            "packages": [],
            "python_version": self._py_version,
        }
        for pkg in self._store.values():
            data["packages"].append(pkg.to_dict())
        contents = json.dumps(data, sort_keys=True, indent=4)
        self._path_save.write_text(contents)
        shutil.move(self._path_save, self._path)

    def __contains__(self, pkg):
        pkg = canonicalize_name(pkg)
        if pkg in self._store:
            return True
        return False

    def __getitem__(self, pkg):
        pkg = canonicalize_name(pkg)
        try:
            return self._store[pkg]
        except KeyError:
            raise DistributionNotFound(f"The '{pkg}' package was not found in store")
