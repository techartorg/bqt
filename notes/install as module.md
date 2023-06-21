### PIP install the latest bqt release
This installs bqt as a module.  less addon clutter, but you need to handle the bqt startup code in your own startup script.  

### console
- use the [[Blender python interpreter]] instead of `python.exe`  
- recommended to install to target path

```commandline
python.exe -m pip install bqt
```
### PIP addon
Instead of the console, you can pip install bqt with the [blender pip addon](https://github.com/hannesdelbeke/blender_pip)
![](https://user-images.githubusercontent.com/3758308/190018745-52fb472c-79a9-46ea-ab85-cf3ab4843ffc.png)

### Installing from Source
If you are installing from a clone of the repository you can easily install by navigating
to bqt's root folder and running:
```commandline
python setup.py install
```
Instead of install from source, you might want to [[setup bqt develop environment]].
