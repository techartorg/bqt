# FAQ

Documentation of some common questions and issues.

## Blender is freezing when I am open the gui.
BQt creates the QApplication for you. 
Do not call `app._exec()` to show widgets,
doing that will freeze Blender.


## Modifier keys no longer works.
This was due to what we used to call "Blender input bug",
it was fixed in #164 which was released in `2.2.0`.
If you are still experiencing this bug after updating please open an issue.


## Running an Operator from PySide doesn't work.
Blender Operators often fail when run from QT, 
because they rely on the active window & other context properties.
But when running a QT tool, the active window is None, leading to an error.

You can fix most of the issues by using a context override, 
either by using BQt's utils or by doing a manual override.

```python
import bqt.utils

@bqt.utils.context_window
def my_method():
    """Do operator magic."""
```

```python
import bpy

def my_method():
    window = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=window):
        """Do operator magic"""
```

## My tool just disappears
This is due to the tool being garbage collected.
Make sure that you haven't set `BQT_AUTO_ADD` to `"0"`.

You can also try to set the parent manually.

```python
from PySide6 import QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.setParent(parent)


app = QtWidgets.QApplication.instance()
app = app.blender_widget if hasattr(app, "blender_widget") else app
w = Window(app)
w.show()
```

## Opening my window twice opens two windows, instead of surfacing the first one.
BQt tries to only keep one of each window around, but for this to work each window
needs a unique objectName.

```python
from PySide6 import QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.setObjectName("my_unqiue_name")
```

