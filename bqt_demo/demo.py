"""
demo to show widget always on top
"""

import sys
from PySide6 import QtCore, QtWidgets


class mymainwindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(parent=None, f=QtCore.Qt.WindowStaysOnTopHint)


app = QtWidgets.QApplication(sys.argv)
mywindow = mymainwindow()
mywindow.show()
app.exec_()
