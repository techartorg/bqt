Installing bqt as an addon means less coding for you.
- The bqt startup code automatically runs on Blender startup.  
- You can disable bqt by disabling the addon.

You can either install through plugget or manually install the addon and its dependencies.

## Plugget  (recommended)

1. Download the [plugget blender addon](https://github.com/hannesdelbeke/plugget-blender-addon/raw/main/installer/install_plugget_addon.blend) by clicking on the link.
2. Find the install file in your downloads folder.
  ![](images/addon_install1.png)
3. Double-clicking the file will automatically open it in Blender.
4. Run the scripts inside to install the addon.
5. Find the Plugget addon by going to `Edit > Preferences > Add-ons`.
6. Type bqt into the search box and click search.
7. Click install. This installs the bqt addon and all its dependencies.
  ![](images/addon_install2.png)


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
