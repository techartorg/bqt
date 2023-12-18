try:
    from PySide6 import QtCore
    from PySide6.QtCore import Qt, QEvent, QObject, QRect, QSettings, QTimer, QDir
    from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QDockWidget, QMessageBox
    from PySide6.QtGui import QCloseEvent, QIcon, QWindow,  QImage, QPixmap
except ImportError:
    try:
        from PySide2 import QtCore
        from PySide2.QtCore import Qt, QEvent, QObject, QRect, QSettings, QTimer, QDir
        from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QDockWidget, QMessageBox
        from PySide2.QtGui import QCloseEvent, QIcon, QWindow,  QImage, QPixmap
    except ImportError:
        pass
