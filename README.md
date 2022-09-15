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

To verify installation was successful, launch Blender and in the python console enter
the following:
```python
from bqt import hello_world
hello_world.demo()
```  

#### Environment Variables
env variables and their default values:
```python
BQT_DISABLE_STARTUP = None  #  test
BQT_TICK_RATE = 30          # 30 ticks per second by default for the qt event loop
BQT_FROM_WIN_ID = False     # if true, blender will be wrapped in a qt window. 
                            # disabled since it causes alt tab bugs, breaking typing in blender
```
## Contribute
If you would like to contribute to bqt, please create a pull request and we will review
the changes
