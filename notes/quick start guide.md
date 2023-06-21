Run this code in Blender for a quick demo.   
(Assumes you have bqt & PySide2 installed, see [[install bqt module]] )

```python
# install bqt and dependencies
# TODO

# run once on startup to setup bqt, not needed if using bqt addon
import bqt
bqt._create_global_app()

# create widget and show it
from PySide2.QtWidgets import QWidget
widget = QWidget()
# bqt.add(widget)  # optional, bqt-autodetect will add the widget automatically
widget.show()
```