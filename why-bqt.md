Custom UI for Python tools in games & VFX often uses QT.<br>
E.g. Maya, Max & Substance all support it natively.<br>
But Blender doesn't. This is where BQT can help.<br>

1. When attempting to run a simple widget, it will crash because we don't have a `QApplication`.
And if you manually `_exec` a new `QApplication`, Blender will freeze untill you close your custom window.

we can parent the widget to the `QAppliciation.instance().blender_widget` which is created by bqt on startup.
2. If we did correclty have a running `QApplication`, it likely would brieflly show the widget, before it dissapears.
This is because it's being garbage collected. Instead of doing a hack saving it to a global variable, 


```python
from PySide2.QtWidgets import QWidget
QWidget().show()
```