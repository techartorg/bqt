When you clone your repo, bqt won't show up in Blender.
To do so, you can either manually copy your modules to Blender's modules path, or copy the add-on code to Blender's addons path.

But to do so every time you make an update is a waste of your time.
A better workflow is to either:
- symlink
- editable package install
- VS-Code Blender extension

## Sym link
- You can create a symlink from your repo to blender's add-on or modules path.
Then any update in the repo auto reflect in Blender on restart of Blender.

```bash
mklink /J "C:\Users\USERNAME\AppData\Roaming\Blender Foundation\Blender\2.93\scripts\addons\bqt" "C:\Users\hanne\OneDrive\Documents\repos\_Blender\bqt\bqt"
```
Pros
- can be used to install bqt as an addon or a module
- saves time copy pasting folders over every time you want to test a change

Cons
- If you symlink the addon and uninstall the addon in Blender, your repo folder might be deleted resulting in loss of uncommitted work.
- Symlink is hard to keep track of when starting to use it in multiple places. I accidentally deleted some work a few times even though "I know what I'm doing"

## Editable package install

Pros
- saves time copy pasting folders over every time you want to test a change
- Cleaner than symlink, doesn't accidentally deletes your work.
- Only works for Python packages. So you can only install bqt as a module, not an add-on. Bqt comes pre-packaged already, with it's `setup.py` file.

Cons
- this only works for packages python modules
- Blender doesn't like editable installs by default, you need to append `sitedir` to the `sys.path` on startup. This can be done automatically on startup with a script in [blender's startup path](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#path-layout) `./scripts/startup/*.py`

## VS-Code Blender extension
TODO investigate, might be able to cleanly install bqt as addon, and trigger real time refresh of script code in Blender.
But you have to start Blender through VS code