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
see [installation docs](https://github.com/techartorg/bqt/wiki/Installation)


### Environment variables
The [bqt env vars](https://github.com/techartorg/bqt/wiki/Environment-variables) let you toggle bqt features on and off

### Sample code
[bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender

### Community
Discuss BQT on 
- the BlenderArtists [thread](https://blenderartists.org/t/bqt-custom-ui-for-add-ons-tool-in-blender-with-pyqt-or-pyside/1458808)
- [Ynput  thread](https://community.ynput.io/t/use-bqt-for-blender-qt-integration/127)

### Alternatives
- Custom (non qt) Blender UI: https://github.com/mmmrqs/bl_ui_widgets
- Blender native UI (N-Panel etc.) [tutorial1](https://b3d.interplanety.org/en/creating-custom-ui-panels-in-blender/) [tutorial2](https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663) 
- Cookie cutter, need to find the link. Some blender devs made a more low level custom UI solution for Blender. Seen at blendcon 22, was a bit buggy though.
