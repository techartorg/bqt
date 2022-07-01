import os
import sys
import types

__version__ = "0.2.0.b2"

QT_VERBOSE = bool(os.getenv("QT_VERBOSE"))
QT_PREFERRED_BINDING = os.environ.get("QT_PREFERRED_BINDING")
QtCompat = types.ModuleType("QtCompat")


def _log(text):
    if QT_VERBOSE:
        sys.stdout.write(text + "\n")


try:
    from PySide2 import (
        QtWidgets,
        QtCore,
        QtGui,
        QtQml,
        QtQuick,
        QtMultimedia,
        QtMultimediaWidgets,
        QtOpenGL,
    )

    from shiboken2 import wrapInstance, getCppPointer
    QtCompat.wrapInstance = wrapInstance
    QtCompat.getCppPointer = getCppPointer

    try:
        from PySide2 import QtUiTools
        QtCompat.loadUi = QtUiTools.QUiLoader

    except ImportError:
        _log("QtUiTools not provided.")


except ImportError:
    try:
        from PyQt5 import (
            QtWidgets,
            QtCore,
            QtGui,
            QtQml,
            QtQuick,
            QtMultimedia,
            QtMultimediaWidgets,
            QtOpenGL,
        )

        QtCore.Signal = QtCore.pyqtSignal
        QtCore.Slot = QtCore.pyqtSlot
        QtCore.Property = QtCore.pyqtProperty

        from sip import wrapinstance, unwrapinstance
        QtCompat.wrapInstance = wrapinstance
        QtCompat.getCppPointer = unwrapinstance

        try:
            from PyQt5 import uic
            QtCompat.loadUi = uic.loadUi
        except ImportError:
            _log("uic not provided.")

    except ImportError:

        # Used during tests and installers
        if QT_PREFERRED_BINDING == "None":
            _log("No binding found")
        else:
            raise

__all__ = [
    "QtWidgets",
    "QtCore",
    "QtGui",
    "QtQml",
    "QtQuick",
    "QtMultimedia",
    "QtMultimediaWidgets",
    "QtCompat",
    "QtOpenGL",
]
