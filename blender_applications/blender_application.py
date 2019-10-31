"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QWindow, QCloseEvent
from PySide2.QtCore import QEvent, QObject, QSettings, QRect

# GLOBALS ###
STYLESHEET_FILEPATH = Path(__file__).parent / 'blender_stylesheet.qss'

SETTINGS_KEY_GEOMETRY = 'Geometry'
SETTINGS_KEY_MAXIMIZED = 'IsMaximized'
SETTINGS_KEY_FULL_SCREEN = 'IsFullScreen'
SETTINGS_WINDOW_GROUP_NAME = 'MainWindow'


class BlenderApplication(QApplication):
    """
    Base Implementation for QT Blender Window Container
    """

    def __init__(self, argv=None):
        argv = [] if argv is None else argv
        super().__init__(argv)

        # System
        self.os_module = self.load_os_module()()

        # QApplication
        if STYLESHEET_FILEPATH.exists():
            self.setStyleSheet(STYLESHEET_FILEPATH.read_text())
        QApplication.setWindowIcon(self.__get_application_icon())

        # Blender Window
        self._hwnd = self.__get_application_hwnd()
        self._blender_window = QWindow.fromWinId(self._hwnd)
        self.blender_widget = QWidget.createWindowContainer(self._blender_window)

        # Variables
        self.should_close = False

        # Runtime
        self.__set_window_geometry()
        self.focusObjectChanged.connect(self.__on_focus_object_changed)

    def notify(self, receiver: QObject, event: QEvent):
        """

        Args:
            receiver: Object to recieve event
            event: Event

        Returns: None

        """
        if isinstance(event, QCloseEvent) and receiver in (self.blender_widget, self._blender_window):
            event.ignore()
            self._store_window_geometry()
            self.should_close = True
            return False

        return super().notify(receiver, event)

    def __on_focus_object_changed(self, focus_object: QObject):
        """

        Args:
            focus_object: Object to track focus event

        Returns: None

        """
        self.os_module.__on_focus_object_changed(focus_object)

    def __set_window_geometry(self):
        """
        Loads stored window geometry preferences and applies them to the QWindow.
        .setGeometry() sets the size of the window minus the window frame.
        For this reason it should be set on self.blender_widget.

        Returns: None

        """
        settings = QSettings('Tech-Artists.org', 'Blender Qt Wrapper')
        settings.beginGroup(SETTINGS_WINDOW_GROUP_NAME)

        if settings.value(SETTINGS_KEY_FULL_SCREEN, 'false').lower() == 'true':
            self.blender_widget.showFullScreen()
            return

        if settings.value(SETTINGS_KEY_MAXIMIZED, 'false').lower() == 'true':
            self.blender_widget.showMaximized()
            return

        self.blender_widget.setGeometry(settings.value(SETTINGS_KEY_GEOMETRY, QRect(0, 0, 640, 480)))
        self.blender_widget.show()

        settings.endGroup()

    def __get_application_hwnd(self):
        """
        This finds the blender application window and collects the
        handler window ID

        Returns int: Handler Window ID
        """
        return self.os_module.__get_application_hwnd()

    def __get_application_icon(self):
        """
        This finds the running blender process, extracts the blender icon from the blender.exe file on disk and saves it to the user's temp folder.
        It then creates a QIcon with that data and returns it.

        Returns QIcon: Application Icon
        """
        return self.os_module.__get_application_icon()

    def __store_window_geometry(self):
        """
        Stores the current window geometry for the QWindow
        The .geometry() method on QWindow includes the size of the application minus the window frame.
        For that reason the _blender_widget should be used.
        """
        settings = QSettings('Tech-Artists.org', 'Blender Qt Wrapper')
        settings.beginGroup(SETTINGS_WINDOW_GROUP_NAME)
        settings.setValue(SETTINGS_KEY_GEOMETRY, self.blender_widget.geometry())
        settings.setValue(SETTINGS_KEY_MAXIMIZED, self.blender_widget.isMaximized())
        settings.setValue(SETTINGS_KEY_FULL_SCREEN, self.blender_widget.isFullScreen())
        settings.endGroup()

    @staticmethod
    def load_os_module():
        """
        Loads the correct OS platform Application Class

        Returns: Instance of BlenderApplication

        """
        operating_system = sys.platform
        if operating_system == 'darwin':
            from .darwin_blender_application import DarwinBlenderApplication
            return DarwinBlenderApplication
        if operating_system in ['linux', 'linux2']:
            # TODO: LINUX module
            pass
        elif operating_system == 'win32':
            from .win32_blender_application import Win32BlenderApplication
            return Win32BlenderApplication
