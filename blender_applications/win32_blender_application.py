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

from PySide2.QtGui import QIcon, QImage, QPixmap
from PySide2.QtCore import QByteArray, QObject

from .blender_application import BlenderApplication

# GLOBALS ###
SETTINGS_KEY_GEOMETRY = 'Geometry'
SETTINGS_KEY_MAXIMIZED = 'IsMaximized'
SETTINGS_KEY_FULL_SCREEN = 'IsFullScreen'
SETTINGS_WINDOW_GROUP_NAME = 'MainWindow'


class Win32BlenderApplication(BlenderApplication):
    """
    Windows implementation of BlenderApplication
    """
    def __init__(self, argv):
        super().__init__(argv)

    def __on_focus_object_changed(self, focus_object: QObject):
        """

        Args:
            QObject focus_object: Object to track focus change
        """
        if focus_object is self.blender_widget:
            win32gui.SetFocus(self._hwnd)

    def __get_application_hwnd(self):
        """
        This finds the blender application window and collects the
        handler window ID

        Returns int: Handler Window ID
        """
        return win32gui.FindWindow(None, 'blender')

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
