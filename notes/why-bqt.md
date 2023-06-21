Custom UI for Python tools in games & VFX often use QT.<br>
Maya, Max & Substance support Qt natively, but Blender doesn't. This is where BQT can help.<br>

Bqt takes care of the heavy lifting, so you can focus on your qt tools.
- manage focus of widgets, letting you parent widgets to blender
- manage QApplication setup for you (the qt eventloop)
- prevent widgets from being garbage collected
- auto style your widgets to match Blender's UI

### More info

```python
from PySide2.QtWidgets import QWidget
QWidget().show()
```

> When attempting to run a simple widget, it will crash because we don't have a `QApplication`.<br>
Manually `_exec` a new `QApplication` freezes Blender untill you close your custom window. (first time only)

- bqt manages the `QApplication` for you, use `QApplication.instance()` to access it if needed.

> - The widget briefly shows & dissapears because it's garbage collected.
> - The widget dissapears behind Blender when you click on Blender

To prevent these issues, parent the widget to ]`QAppliciation.instance().blender_widget` (blender_widget is created by bqt on startup).
