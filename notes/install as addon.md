
# #TODO 👷add step by step images

## install bqt as a addon (recommended)
It's recommended to install bqt as an addon, since startup code is then handled automatically for you when the addon is enabled in Blender.

1. Download the latest release. You can download the zip from the repo.
2. Extract the zip and copy the `bqt` folder to your blender addons folder.
3. (ADVANCED) Ensure the dependencies are installed from `requirements.txt`  
   
   Use the [[Blender python interpreter]] instead of `python`
```bash
cd "your/bqt/folder/path"
python -m pip install -r requirements.txt
```
4. Enable the addon by going to `Edit > Preferences > Add-ons` and search for `qt`

