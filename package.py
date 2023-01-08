from shutil import copytree, make_archive, rmtree
import subprocess as sp
from pathlib import Path
from platform import platform, python_version

ADDON_NAME = "bqt"
PARENT_DIR = Path(__file__).parent
PKG_DIR = PARENT_DIR / "target"

# Delete existing "out" directory
if PKG_DIR.exists():
    if PKG_DIR.is_dir():
        rmtree(PKG_DIR)
    else:
        raise RuntimeError("Output directory exists and it is not a directory")

copytree(PARENT_DIR / ADDON_NAME, PKG_DIR / "archive" / ADDON_NAME)

sp.run(
    [
        "pip",
        "install",
        "-r",
        PARENT_DIR / "requirements.txt",
        "-t",
        PKG_DIR / "archive" / ADDON_NAME / "vendor",
    ]
)

# Create addon ZIP
zip_filename = f"{ADDON_NAME}-{python_version()}-{platform()}"
zip_filepath = (PKG_DIR / zip_filename).as_posix()
make_archive(zip_filepath, "zip", root_dir=PKG_DIR / "archive")
