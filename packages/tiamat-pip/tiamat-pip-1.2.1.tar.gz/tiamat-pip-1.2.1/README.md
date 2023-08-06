# Tiamat Pip

Pip handling for tiamat projects

## Setup
In order to be able to `pip install` packages which can be used with your tiamat packaged application
you need to add `tiamat-pip` as a dependency and your `run.py` should look similar to:

```python
#!/usr/bin/env python3

import sys
import multiprocessing

import tiamatpip.cli
import tiamatpip.configure

import mainapp

# Configure the path where to install the new packages
tiamatpip.configure.set_user_site_packages_path("THIS SHOULD BE A HARDCODED PATH")


def main(argv):
    # Let's see if we should be handling pip related stuff
    if tiamatpip.cli.should_redirect_argv(argv):
        tiamatpip.cli.process_pip_argv(argv)

    # If we reached this far, it means we're not handling pip stuff
    # Your application logic can resume

    mainapp.main(argv)
    sys.exit(0)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        multiprocessing.freeze_support()
    main(sys.argv)
```
