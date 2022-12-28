# bqt
Add QT support to Blender, letting you create custom UI for your addons with PySide2 QtWidgets.

## Requirements
Blender `2.83`or higher.
Windows or Mac


## Installation  

### PIP install
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
- BQT_DISABLE_STARTUP if set, completely disable bqt
- BQT_DISABLE_WRAP if set to 1, disable wrapping blender in a QWindow
- BQT_DISABLE_CLOSE_DIALOGUE if set to 1, use the standard blender close dialogue

### Sample code
[bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender

### Supported Platforms  
bqt is developed on Windows, but also supports Darwin (MacOS).
If you are a dev, add a PR for another OS.
