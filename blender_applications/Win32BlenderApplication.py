"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import bpy
import win32con
import win32api
import win32gui
import win32ui

from PySide2.QtGui import QCloseEvent, QIcon, QImage, QPixmap
from PySide2.QtCore import QByteArray, QEvent, QObject, QRect, QSettings

from bqt import BlenderApplication

# GLOBALS ###
SETTINGS_KEY_GEOMETRY = 'Geometry'
SETTINGS_KEY_MAXIMIZED = 'IsMaximized'
SETTINGS_KEY_FULL_SCREEN = 'IsFullScreen'
SETTINGS_WINDOW_GROUP_NAME = 'MainWindow'


class Win32BlenderApplication(BlenderApplication):
    """
    Windows implementation of BlenderApplication
    """

    def notify(self, receiver: QObject, event: QEvent):
        if isinstance(event, QCloseEvent) and receiver in (self.blender_widget, self._blender_window):
            event.ignore()
            self._store_window_geometry()
            self.should_close = True
            return False

        return super().notify(receiver, event)

    def __on_focus_object_changed(self, focus_object: QObject):
        """

        Args:
            QObject focus_object: Object to track focus change
        """
        if focus_object is self.blender_widget:
            win32gui.SetFocus(self._hwnd)

    def __set_window_geometry(self):
        """
        Loads stored window geometry preferences and applies them to the QWindow.
        .setGeometry() sets the size of the window minus the window frame.
        For this reason it should be set on self.blender_widget.

        Returns:

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

    def __get_application_icon(self) -> QIcon:
        """
        This finds the running blender process, extracts the blender icon from the blender.exe file on disk and saves it to the user's temp folder.
        It then creates a QIcon with that data and returns it.

        Returns: QImage icon

        """
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        large, _small = win32gui.ExtractIconEx(bpy.app.binary_path, 0)
        hdc.DrawIcon((0, 0), large[0])
        bmp_str = hbmp.GetBitmapBits(True)

        img = QImage()
        img.loadFromData(QByteArray(bmp_str))

        return QIcon(QPixmap(img))

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