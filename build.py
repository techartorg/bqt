from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path
from site import getsitepackages
import sys
from shutil import copy


class CustomInstall(install):
    """ """

    def run(self):
        # Run the standard PyPi Copy
        install.run(self)

        # Post install logic:

        # Copy the bqt_startup.py to the blender scripts/startup so that
        # bqt will initialize properly at Blender startup
        startup_file_path = next(
            (Path(pkg) / "dist" / "bqt_startup.py" for pkg in getsitepackages() if "site-packages" in pkg),
            None,
        )
        if not startup_file_path:
            print("bqt_startup.py was not found. Please manually move bqt_startup.py to scripts/startup")
            return
        if not startup_file_path.is_file():
            print("bqt_startup.py was not found. Please manually move bqt_startup.py to scripts/startup")
            return
        # Get the file destination path
        destination_path = Path(sys.executable).parents[2] / "scripts" / "startup"

        if not destination_path.exists() and not destination_path.is_dir():
            print("Bqt didn't get installed in a Blender Python environment, skipping further setup.")
            return

        # Copy the file to destination path
        copy(startup_file_path, destination_path)

        # Validate that the file was copied properly
        if (destination_path / "bqt_startup.py").is_file():
            print(f"Successfully copied bqt_startup.py to {destination_path}")
        else:
            print(f"bqt_startup.py was not copied to {destination_path}.")
