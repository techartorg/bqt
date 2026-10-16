## Local development of bqt
This is how you can set up a local testing environment for bqt.

This will clone the repository, create a venv, link the cloned repository to the venv so that when you start up Blender your working copy is used. Any changes you do locally to bqt will be picked up after you (re)start Blender through the command.

**Requirements**:
* [uv](https://docs.astral.sh/uv/) installed.
* Windows

### Prepare project folder
Create a directory for our files. This will host our clone of bqt, our venv that will be used inside of blender and our startup script.
```
mkdir bqt-project
``` 

Change directory
```
cd bqt-project
``` 

### Clone bqt
Clone the project using either ssh or http.

> [!NOTE]
> Only do one, they are both here only for convenience.

```
git clone git@github.com:techartorg/bqt.git
```
```
git clone https://github.com/techartorg/bqt.git
```
### Create and prepare our virtual environment
Create a venv that we will use inside of Blender. 

> [!IMPORTANT]
> The version here is important. We use `3.11.13` as that's the version Blender 5.0.1. is using. If you are using an older version you should use a different python version.

```
uv venv --python 3.11.13
```

As we want to install things into the venv as well as run tools from it we activate it.
```
.venv\Scripts\activate.bat
```

Install python-dot env, we will use this to load our .env file.
```
uv pip install python-dotenv[cli]
```

Install the copy of bqt we cloned as an [editable package](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), any changes to bqt will be picked up every time we restart Blender.
```
uv pip install --editable .\bqt\
```

### Add a startup script
Create a folder for our startup script. This script will enable bqt on Blender startup.
```
mkdir -p scripts\startup
```

Add a startup script.

> [!NOTE]
> This is very basic and technically not how you should use an addon. You will get a warning in your log, feel free to fix this file manually to get rid of the warning.

```
echo import bqt > scripts/startup/bqt_enable.py && echo bqt.register() >> scripts/startup/bqt_enable.py
```

### Add variables to our local environment
We need to set some environment variables for Blender to properly pick up our venv. We echo these into a .env file which we will source by using `dotenv run` later.

> [!TIP]
> You can edit this file normally to add any `BQT_` environment variables you want to launch Blender with.

This one adds our virtual environment site-packages to the python path, this way python will be able to find installed packages.
```
echo PYTHONPATH=%cd%\.venv\Lib\site-packages;%cd%\bqt > .env
```
This makes sure that Blender finds out startup script.
```
echo BLENDER_SYSTEM_SCRIPTS=%cd%\scripts >> .env
```
This ensures that our virtual environment is the first in the PATH variable, that way our venv scripts will be the first ones found.
```
echo PATH=%cd%\.venv\Scripts;%PATH% >> .env
```
### Launching blender
You can now start Blender. Change the `blender.exe` to your Blender path (or add the folder the blender.exe is in to your PATH variable). As always if you have spaces in your path you will need to put the whole path inside quotes `"`.
```
dotenv run -- blender.exe --python-use-system-env
```

### Coming back to work
Now when ever you want to work on Blender you only need to run the above command through a shell that has the venv activated. If you ever close down your shell you only need to change directory, activate the venv, run Blender with dotenv.

> [!TIP]
> You can put these into bat file and use that to launch your bqt dev environment.

```
cd bqt-project
``` 
```
.venv\Scripts\activate.bat
```
```
dotenv run -- blender.exe --python-use-system-env
```