##Problem

The exact same code might behave different when executed from the script editor compared to when executed after pressing a QT button.

Blender Operators often fail when run from QT, because they rely on the active window & other context properties.
But when running a QT tool, the active window is None, leading to an error.

## Fix

### context override

#### bqt utils
bqt ships with a decorator you can add to your functions, like this:
```python
import bqt.utils

@bqt.utils.context_window
def my_method():
    do operator magic
```
This will fix the majority of issues, but not all of them.
You can also do the exact same manually, with a context override.

#### manual context override
To work around this, you can [override the context](https://docs.blender.org/api/current/bpy.ops.html#overriding-context). 

e.g. this is what happens under the hood of the above decorator
```python
window = bpy.context.window_manager.windows[0]
with bpy.context.temp_override(window=window):
    original_code ...
```

to override additional context properties, just add them to the temp_override:

```python
with bpy.context.temp_override(window=window, object=obj, active_object=obj):
```



