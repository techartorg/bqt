Custom UI for Python tools in games & VFX often uses QT.<br>
E.g. Maya, Max & Substance all support it natively.<br>
But Blender doesn't. This is where BQT can help.<br>

```python
from PySide2.QtWidgets import QWidget
QWidget().show()
```

> When attempting to run a simple widget, it will crash because we don't have a `QApplication`.<br>
Manually `_exec` a new `QApplication` freezes Blender untill you close your custom window. (first time only)

bqt manages the `QApplication` for you, use `QApplication.instance()` to access it if needed.
 
> - The widget briefly shows & dissapears because it's garbage collected.
> - The widget dissapears behind Blender when you click on Blender

To prevent these issues, parent the widget to ]`QAppliciation.instance().blender_widget` (blender_widget is created by bqt on startup).
