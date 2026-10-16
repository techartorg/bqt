# Installing

There are multiple ways to install BQt.

* As an [Isolated environment](#isolated-environment), recommended for studios.
* As an [Addon through Plugget](#addon-through-plugget), recommended for single users.
* As a [module directly into Blenders python](#into-the-interpreter), as an alternative to plugget.

## Isolated environment
This is our recommendation for studios as it doesn't modify the blender installation.

1. Create a virtual environment.
2. Activate it by setting the needed Environment Variables.
3. Install BQt and any other required dependencies.
4. Create a startup script that activates BQt.
5. Start Blender with the `--python-use-system-env` flag.

This script is only an example. Adopt it to your own studios need.

## `blender.bat`

```bash
@ECHO OFF

if not exist %USERPROFILE%\.bqt (
  mkdir %USERPROFILE%\.bqt
)

if not exist %USERPROFILE%\.bqt\.venv (
  REM This python version needs to be consistent your Blender versions python.
  uv venv --python 3.11.13  %USERPROFILE%\.bqt\.venv
)

if not exist %USERPROFILE%\.bqt (
  mkdir %USERPROFILE%\.bqt
)

set VIRTUAL_ENV=%USERPROFILE%\.bqt\.venv
set VIRTUAL_ENV_PROMPT=bqt
set PATH=%USERPROFILE%\.bqt\.venv\Scripts;%PATH%
set PYTHONPATH=%USERPROFILE%\.bqt\.venv\Lib\site-packages;%PYTHONPATH%
set BLENDER_SYSTEM_SCRIPTS=%USERPROFILE%\.bqt\scripts

REM We are echoing our version into compile to get the latest version. Then we sync the output.
REM In a studio environment you might instead want to supply a requirements file to pip compile. 
echo bqt==2.* | uv pip compile - | uv pip sync -

if not exist %USERPROFILE%\.bqt\scripts\startup (
  mkdir %USERPROFILE%\.bqt\scripts\startup
)

if not exist %USERPROFILE%\.bqt\scripts\startup\bqt_enable.py (
  (
    echo import bqt
	echo bqt.register(^)
  ) > %USERPROFILE%\.bqt\scripts\startup\bqt_enable.py
)
  
REM Update this to your own Blender path.
"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --python-use-system-env
```

## Addon through [Plugget](https://github.com/plugget)
Installing BQt as an addon through plugget is an alternative, a good alternative for a single user.
However, it will modify your blender's python interpreter packages.

1. Download the [plugget blender addon](https://github.com/hannesdelbeke/plugget-blender-addon/raw/main/installer/install_plugget_addon.blend)
by clicking on the link.
2. Find the installation file in your Downloads folder.
![](/docs/assets/addon_install1.png)
3. Double-clicking the file will automatically open it in Blender.
4. Run the scripts inside to install the addon.
5. Find the Plugget addon by going to Edit > Preferences > Add-ons.
6. Type BQt into the search box and click search.
7. Click install. This installs the BQt addon and all its dependencies.
![](/docs/assets/addon_install2.png)


## Into the interpreter
Installing directly to the interpreter isn't recommended but a possibility for a quick and dirty set up.

1. Locate your Blenders python interpreter `../Blender Foundation/Blender <version>/<version>/Python/bin/python.exe`
2. Use it to install BQt. `<path-to-python-exe> -m pip install bqt`
3. Locate your blender scripts folder and in the startup folder create a startup script.
    ```python
    import bqt
    bqt.register()
    ```
