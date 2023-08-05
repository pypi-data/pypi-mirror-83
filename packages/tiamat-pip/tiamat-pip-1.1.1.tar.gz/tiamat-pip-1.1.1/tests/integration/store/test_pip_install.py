"""
    tests.integration.store.test_pip_install
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the tiamat-pip installation store.
    This store holds information about the pip installed packages which
    can be used to re-install all of them in case the tiamat package python
    version is upgraded.
"""


def test_pop_config(project):
    """
    The actual package name is pop-config, however we're using pop_config
    to confirm we can properly resolve package names like pip does.
    """
    pkg_name = "pop_config"
    real_package_name = "pop-config"

    # Install pep8 so that the store is not empty
    ret = project.run("pip", "install", "pep8")
    assert ret.exitcode == 0
    assert "pep8" in project.get_store()

    # pop-config is not installed
    ret = project.run("pip", "list")
    assert ret.exitcode == 0
    assert real_package_name not in ret.stdout

    ret = project.run("pip", "install", pkg_name)
    assert ret.exitcode == 0
    ret = project.run("pip", "list")
    assert real_package_name in ret.stdout
    assert real_package_name in project.get_store()
    # pop-config relies on pop, so we want to see it in the pip list output
    assert "pop" in ret.stdout
    # But we do not want to see it recorded in the store since it's not a
    # "top level" requirement.
    assert "pop" not in project.get_store()

    ret = project.run("pip", "uninstall", "-y", pkg_name)
    assert ret.exitcode == 0

    ret = project.run("pip", "list")
    assert ret.exitcode == 0
    assert real_package_name not in ret.stdout
    assert pkg_name not in ret.stdout
    assert real_package_name not in project.get_store()
    assert pkg_name not in project.get_store()

    # The store should still contain pep8
    assert "pep8" in project.get_store()
