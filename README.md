# bqt



[![PyPI version](https://img.shields.io/pypi/v/bqt)](https://pypi.org/project/bqt/)
[![latest tag](https://img.shields.io/github/v/tag/techartorg/bqt?label=Github)](https://github.com/techartorg/bqt) ⚠️ PyPi version is currently outdated. Install from this repo for latest.


Add QT support to Blender, letting you create custom UI for your addons with PySide2 QtWidgets.

## Requirements
Blender `2.83`or higher.
Windows (stable) or Mac (experimental)


## Installation  

### install as addon
1. Download the latest release. You can download the zip from the repo.
2. Extract the zip and copy the `bqt` folder to your blender addons folder.
3. Enable the addon by going to `Edit > Preferences > Add-ons` and search for `qt`

### PIP install
⚠ PIP install is currently outdated, do not use until further notice.

The installation of bqt with automatic setup for Blender requires the usage of the integrated python
interpreter found within `../Blender Foundation/<version>/Python/bin`
```commandline
python.exe -m pip install bqt
```

### Installing from Source
If you are installing from a clone of the repository you can easily install by navigating
to bqt's root folder and running:
```commandline
python setup.py install
```


# Developers

### Environment variables
- BQT_DISABLE_STARTUP if set to 1, completely disable bqt
- BQT_DISABLE_WRAP if set to 1, disable wrapping blender in a QWindow
- BQT_DISABLE_CLOSE_DIALOGUE if set to 1, use the standard blender close dialogue

### Sample code
[bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender
