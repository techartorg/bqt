Blender Operators often fail when run from QT, because they rely on the active window & other context properties.
But when running a QT tool, the active window is None.

To work around this, you can [override the context](https://docs.blender.org/api/current/bpy.ops.html#overriding-context). 
```python
window = bpy.context.window_manager.windows[0]
with bpy.context.temp_override(window=window):
    original_code ...
```
to override additional context properties:
```python
with bpy.context.temp_override(window=window, object=obj, active_object=obj):
```

TLDR: the exact same code might behave different when executed from the script editor compared to when executed after pressing a QT button.