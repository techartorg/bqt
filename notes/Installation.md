describe pros and cons of addon vs module install
- addon can be disabled
- module install means less addon clutter, but need to manage the bqt setup in your own startup script.

### install bqt as a addon (recommended)
It's recommended to install bqt as an addon, since startup code is then handled automatically for you when the addon is enabled in Blender.

1. Download the latest release. You can download the zip from the repo.
2. Extract the zip and copy the `bqt` folder to your blender addons folder.
3. Enable the addon by going to `Edit > Preferences > Add-ons` and search for `qt`

### PIP install the latest bqt release
This installs bqt as a module.
You need to handle bqt startup code in your own startup script.

⚠️ The installation of bqt requires the usage of Blender's integrated Python interpreter.
You can find it in your Blender install folder: `../Blender Foundation/<version>/Python/bin`

```commandline
python.exe -m pip install bqt
```

### Installing from Source
If you are installing from a clone of the repository you can easily install by navigating
to bqt's root folder and running:
```commandline
python setup.py install
```
Instead of install from source, you might want to [[setup bqt develop environment]].
