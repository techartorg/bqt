# bqt.py  
This is a blender startup script that allows for creating PySide2 based QtWidgets from within blender.

## Requirements
Due to the release of `Blender 2.83 LTS`, the minimum Blender version required for bqt is `2.83`.
This is based on the updated python support that is now packaged with the base install.  

#### Supported Platforms  
bqt is currently in development for Windows and Darwin (MacOS), however our primary
focus and main stream of support is within the Windows environment.

## Installation  
The installation of bqt with automatic setup for Blender requires the usage of the integrated python
interpreter found within `../Blender Foundation/<version>/Python/bin`
```commandline
python.exe -m pip insteall bqt
```

#### Installing from Source
If you are installing from a clone of the repository you can easily install by navigating
to bqt's root folder and running:
```commandline
python setup.py install
```

### Sample code
[bqt_demo](bqt_demo) shows you how to use bqt with several qt demos you can run in Blender

## Contribute
If you would like to contribute to bqt, please create a pull request and we will review
the changes
