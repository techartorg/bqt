Installing bqt as an addon means less coding for you.
- The bqt startup code automatically runs on Blender startup.  
- you can disable bqt by disabling the addon

You can either install through plugget, or manually install the addon and it's dependencies.

## Plugget  (recommended)

#TODO 👷add step by step images

1. Install the [plugget blender addon](https://github.com/hannesdelbeke/plugget-blender-addon)
2. search bqt and click install. This auto installs the bqt addon and all it's dependencies.


## manual add-on install

#TODO 👷add step by step images

1. Download the latest release. You can download the zip from the repo.
2. Extract the zip and copy the `bqt` folder to your blender addons folder.
3. (ADVANCED) Ensure the dependencies are installed from `requirements.txt`  
   
   Use the [[Blender python interpreter]] instead of `python`
```bash
cd "your/bqt/folder/path"
python -m pip install -r requirements.txt
```
4. Enable the addon by going to `Edit > Preferences > Add-ons` and search for `qt`

