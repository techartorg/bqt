try:
    from PySide6 import QtCore
    from PySide6.QtCore import Qt, QEvent, QObject, QRect, QSettings, QTimer, QDir
    from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QDockWidget, QMessageBox
    from PySide6.QtGui import QCloseEvent, QIcon, QWindow,  QImage, QPixmap
    print("BQT imported PySide6")
except ImportError:
    try:
        from PySide2 import QtCore
        from PySide2.QtCore import Qt, QEvent, QObject, QRect, QSettings, QTimer, QDir
        from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QDockWidget, QMessageBox
        from PySide2.QtGui import QCloseEvent, QIcon, QWindow,  QImage, QPixmap
        print("BQT imported PySide2")
    except ImportError:
        print("BQT failed to import PySide")
        pass

# __all__ enables support for import from, e.g. 'from qt_core import QWindow'
# the above import adds it to the local namespace, _all__ adds it to the module public namespace
__all__ = [
    "Qt", "QEvent", "QObject", "QRect", "QSettings", "QTimer", "QDir",
    "QApplication", "QWidget", "QMainWindow", "QDockWidget", "QMessageBox",
    "QCloseEvent", "QIcon", "QWindow", "QImage", "QPixmap", "QtCore"
]
