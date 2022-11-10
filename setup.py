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
"""
import os
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from shutil import copy
from site import getsitepackages
from subprocess import Popen
import sys


class CustomInstall(install):
    """ """

    def run(self):
        # Run the standard PyPi Copy
        install.run(self)

        # Post install logic:

        # Copy the bqt_startup.py to the blender scripts/startup so that
        # bqt will initialize properly at Blender startup
        startup_file_path = None
        # Find the blender site-packages folder and generate the full path to bqt_startup.py
        for pkg in getsitepackages():
            if "site-packages" in pkg:
                startup_file_path = Path(pkg) / "bqt" / "dist" / "bqt_startup.py"
                break

        if not os.path.isfile(startup_file_path):
            print("bqt_startup.py was not found. Please manually move bqt_startup.py to scripts/startup")
            return

        # Get the file destination path
        destination_path = Path(sys.executable).parents[2] / "scripts" / "startup"

        if not os.path.exists(destination_path) and not os.path.isdir(destination_path):
            print("Bqt didn't get installed in a Blender Python environment, skipping further setup.")
            return

        # Copy the file to destination path
        copy(startup_file_path, destination_path)

        # Validate that the file was copied properly
        if os.path.isfile(destination_path / "bqt_startup.py"):
            print(f"Successfully copied bqt_startup.py to {destination_path}")
        else:
            print(f"bqt_startup.py was not copied to {destination_path}.")


setup(
    # Metadata
    name="bqt",
    version="0.2.0",
    description="Files to help bootstrap PySide2 with an event loop within Blender.",
    keywords=["Technical", "Art", "TechArt", "TechArtOrg", "Blender", "Qt", "PySide"],
    license="Mozilla Public License 2.0 (MPL 2.0)",
    url="https://github.com/techartorg/bqt",
    author="tech-artists.org",
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3.7",
    ],
    # Requirements
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=["PySide2"],
    # Package Data
    include_package_data=True,
    package_data={"bqt": ["*.png", "*.qss", "dist/bqt_startup.py"]},
    # Install Wrapper
    cmdclass={"install": CustomInstall},
)
