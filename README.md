# BQt

[![PyPI version](https://img.shields.io/pypi/v/bqt)](https://pypi.org/project/bqt/)
[![latest tag](https://img.shields.io/github/v/tag/techartorg/bqt?label=Github)](https://github.com/techartorg/bqt)
[![](https://img.shields.io/badge/GitHub-Wiki-blue)](https://github.com/techartorg/bqt/wiki)

Add QT support to Blender, letting you create custom UI for your addons with PySide2 QtWidgets.
![custom ui sample](https://user-images.githubusercontent.com/3758308/192096952-e9ed73be-26e4-4ad8-a85f-be4175cebbda.gif)

## Features
| feature | description|
|--|--|
|fully custom UI |Instead of feeling limited by N-Panel only UI. Do whatever you want. |
| cross app | Qt widgets run nativaly in Krita, 3ds Max, Maya, … and are great to use in cross dcc pipelines |
| existing community | hundreds of QT widgets on GitHub you can reuse, and lots of stack exchange questions answered regarding qt.|
|Themed | BQt applies the [blender-qt-stylesheet](https://github.com/hannesdelbeke/blender-qt-stylesheet) so qt widgets will by default look similar to Blender.|


## Requirements
- Blender `2.83`or higher.
- Windows or Mac
- PySide2
- `PyObjC` & `iterm2` (Mac only)

## How to use
1. Install & enable the bqt addon (see [installation docs](https://github.com/techartorg/bqt/wiki/Installation))
2. Create & show your Qt widget, bqt will automatically register it with it's widget manager.

- The [bqt env vars](https://github.com/techartorg/bqt/wiki/Environment-variables) let you toggle bqt features on and off
- sample code: [bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender

### contribute
- i'm a technical writer and want to contribute to the docs. see [readme](https://github.com/techartorg/bqt/wiki/README) on the wiki.
- i'm a dev and want to contribute to bqt code, see [contribute guidelines](https://github.com/techartorg/bqt/wiki/contribute-guidelines).
- i'm a user or tester and want to report a bug or request a feature, please post [here](https://github.com/techartorg/bqt/issues)

### Community
Discuss BQt on 
- the BlenderArtists [thread](https://blenderartists.org/t/bqt-custom-ui-for-add-ons-tool-in-blender-with-pyqt-or-pyside/1458808)
- [Ynput  thread](https://community.ynput.io/t/use-bqt-for-blender-qt-integration/127)
