"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

**Generating Distribution Archives:**
https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives

** Uploading Distribution Archives:**
https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives

**Notes:**
    In order for the Custom Install wrapper to run successfully we have to use the source distribution
    when we are building our archives. This is done by running the command:
        python setup.py sdist

    This creates a *.tar.gz source file that we use to send to PyPi/TestPyPi that will run setup.py
    compared to shipping a wheel, *.whl, which is binary and does not run any post-install logic.

**Contributors:**
    Greg Amato, amatobahn@gmail.com, June 18, 2020.
    Mel Massadian, mel@melmassadian.com, January 2023.
"""

import setuptools

if __name__ == "__main__":
    setuptools.setup()
