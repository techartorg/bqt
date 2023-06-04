"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from abc import abstractmethod, abstractstaticmethod, ABCMeta
from pathlib import Path
import os
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QCloseEvent, QIcon, QImage, QPixmap, QWindow
from PySide2.QtCore import QEvent, QObject, QRect, QSettings
from bqt.ui.quit_dialogue import BlenderClosingDialog
import bpy


STYLESHEET_PATH = Path(__file__).parents[1] / "blender_stylesheet.qss"
ORGANISATION = "Tech-Artists.org"
APP = "Blender Qt"
WINDOW_TITLE = "Blender Qt"
WINDOW_GROUP_NAME = "MainWindow"
GEOMETRY = "Geometry"
MAXIMIZED = "IsMaximized"
FULL_SCREEN = "IsFullScreen"


class BlenderApplication(QApplication):
    """
    Base Implementation for QT Blender Window Container
    """

    def __init__(self, *args, **kwargs):
        __metaclass__ = ABCMeta
        super().__init__(*args, **kwargs)

        if STYLESHEET_PATH.exists():
            self.setStyleSheet(STYLESHEET_PATH.read_text())

        QApplication.setWindowIcon(self._get_application_icon())

        # Blender Window
        self._hwnd = self._get_application_hwnd()
        failed_to_get_handle = self._hwnd is None

        if os.getenv("BQT_DISABLE_WRAP") == "1" or failed_to_get_handle:
            self._blender_window = QWindow()
            self.blender_widget = QWidget.createWindowContainer(self._blender_window)
        else:
            self._blender_window = QWindow.fromWinId(self._hwnd)  # also sets flag to Qt.ForeignWindow
            self.blender_widget = QWidget.createWindowContainer(self._blender_window)
            self.blender_widget.setWindowTitle(WINDOW_TITLE)
            self._set_window_geometry()
            self.focusObjectChanged.connect(self._on_focus_object_changed)

    @abstractstaticmethod
    def _get_application_hwnd() -> int:
        """
        This finds the blender application window and collects the
        handler window ID

        Returns int: Handler Window ID
        """

        return -1

    @staticmethod
    def _get_application_icon() -> QIcon:
        """
        This finds the running blender process, extracts the blender icon from the blender.exe file on disk and saves it to the user's temp folder.
        It then creates a QIcon with that data and returns it.

        Returns QIcon: Application Icon
        """

        icon_filepath = Path(__file__).parents[1] / "images" / "blender_icon_16.png"
        icon = QIcon()

        if icon_filepath.exists():
            image = QImage(str(icon_filepath))
            if not image.isNull():
                icon = QIcon(QPixmap().fromImage(image))

        return icon

    @abstractmethod
    def _on_focus_object_changed(self, focus_object: QObject):
        """
        Args:
            focus_object: Object to track focus event
        """

        pass

    def _unwrapped_window_geometry(self) -> QRect:
        """
        Get the window geometry from the Blender window before it was wrapped in a QWidgetContainer
        Run this before wrapping the window in a QWidgetContainer
        Returns QRect(x, y, width, height)
        """
        window = bpy.context.window_manager.windows[0]
        height, widht = window.height, window.width
        x = window.x
        y = window.y  # blender y relative from bottom of screen to bottom of Blender window
        # convert y to be relative from the top
        current_screen_rect = self.primaryScreen().availableGeometry()
        y = current_screen_rect.height() - y - height
        y += 56  # title bar offset
        return QRect(x, y, widht, height)


    def _set_window_geometry(self):
        """
        Loads stored window geometry preferences and applies them to the QWindow.
        .setGeometry() sets the size of the window minus the window frame.
        For this reason it should be set on self.blender_widget.
        """
        settings = QSettings(ORGANISATION, APP)
        settings.beginGroup(WINDOW_GROUP_NAME)
        fullscreen = settings.value(FULL_SCREEN, defaultValue=False, type=bool)
        maximized = settings.value(MAXIMIZED, defaultValue=False, type=bool)
        saved_geometry = settings.value(GEOMETRY)
        settings.endGroup()

        if fullscreen:
            self.blender_widget.showFullScreen()
            return

        if maximized:
            self.blender_widget.showMaximized()
            return


        unwrapped_geometry = self._unwrapped_window_geometry()  # maintain unwrapped window size & pos
        geometry = saved_geometry or unwrapped_geometry  # if no saved geometry, use previous blender window size
        self.blender_widget.setGeometry(geometry)  # setGeometry is relative to its parent

        self.blender_widget.show()

    def notify(self, receiver: QObject, event: QEvent) -> bool:
        """
        Args:
            receiver: Object to receive event
            event: Event

        Returns: bool
        """

        if isinstance(event, QCloseEvent) and receiver in (self.blender_widget, self._blender_window):
            # catch the close event when clicking close on the qt window,
            # ignore the event, and ask user if they want to close blender if unsaved changes.
            # if this is successful, blender will trigger bqt.on_exit()
            event.ignore()

            if os.getenv("BQT_DISABLE_CLOSE_DIALOGUE") == "1":
                # this triggers the default blender close event, showing the save dialog if needed
                bpy.ops.wm.quit_blender({"window": bpy.context.window_manager.windows[0]}, "INVOKE_DEFAULT")
            else:
                closing_dialog = BlenderClosingDialog(self.blender_widget)
                closing_dialog.execute()

            return False

        return super().notify(receiver, event)

    def store_window_geometry(self):
        """
        Stores the current window geometry for the QWindow
        The .geometry() method on QWindow includes the size of the application minus the window frame.
        For that reason the _blender_widget should be used.
        """

        settings = QSettings(ORGANISATION, APP)
        settings.beginGroup(WINDOW_GROUP_NAME)
        settings.setValue(GEOMETRY, self.blender_widget.geometry())
        settings.setValue(MAXIMIZED, self.blender_widget.isMaximized())
        settings.setValue(FULL_SCREEN, self.blender_widget.isFullScreen())
        settings.endGroup()
