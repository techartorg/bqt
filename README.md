# bqt



[![PyPI version](https://img.shields.io/pypi/v/bqt)](https://pypi.org/project/bqt/)
[![latest tag](https://img.shields.io/github/v/tag/techartorg/bqt?label=Github)](https://github.com/techartorg/bqt)


Add QT support to Blender, letting you create custom UI for your addons with PySide2 QtWidgets.
![custom ui sample](https://user-images.githubusercontent.com/3758308/192096952-e9ed73be-26e4-4ad8-a85f-be4175cebbda.gif)

## Features
| feature | description|
|--|--|
|fully custom UI |Instead of feeling limited by N-Panel only UI. Do whatever you want. |
| cross app | Qt widgets run nativaly in Krita, 3ds Max, Maya, … and are great to use in cross dcc pipelines |
| existing community | hundreds of QT widgets on GitHub you can reuse, and lots of stack exchange questions answered regarding qt.|
|Themed | BQT ships with a basic blender theme, so qt widgets will by default look similar to Blender.|


## Requirements
Blender `2.83`or higher.
Windows (stable) or Mac (experimental)


## Installation  

### install as addon (recommended)
1. Download the latest release. You can download the zip from the repo.
2. Extract the zip and copy the `bqt` folder to your blender addons folder.
3. Enable the addon by going to `Edit > Preferences > Add-ons` and search for `qt`

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

## Develop setup
When working on the bqt code from a repo, to prevent having to reinstall bqt every time you make a change,
you can symlink the bqt folder to your blender addons folder to develop bqt. 
Any updates in the repo are then reflected in blender on restart.
e.g.:
```commandline
mklink /J "C:\Users\USERNAME\AppData\Roaming\Blender Foundation\Blender\2.93\scripts\addons\bqt" "C:\Users\hanne\OneDrive\Documents\repos\_Blender\bqt\bqt"
```

### Environment variables
| variable | description|
|--|--|
|BQT_DISABLE_STARTUP| if set to `1`, completely disable bqt|
|BQT_DISABLE_WRAP| if set to `1`, disable wrapping blender in a QWindow|
|BQT_DISABLE_CLOSE_DIALOGUE| if set to `1`, use the standard blender close dialogue|
|BQT_MANAGE_FOREGROUND| defaults to `1`, if `0`, widgets registered with `bqt.add(my_widget)` won't stay in the foreground when using Blender.|
if you modify env vars, ensure they're strings

### Sample code
[bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender

### Community
Discuss BQT on 
- the BlenderArtists [thread](https://blenderartists.org/t/bqt-custom-ui-for-add-ons-tool-in-blender-with-pyqt-or-pyside/1458808)
- [Ynput  thread](https://community.ynput.io/t/use-bqt-for-blender-qt-integration/127)

### ALternative
- Custom UI for Blender only: https://github.com/mmmrqs/bl_ui_widgets
