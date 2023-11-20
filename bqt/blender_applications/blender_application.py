"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import logging
from abc import abstractmethod, abstractstaticmethod, ABCMeta
import os
from bqt.ui.quit_dialogue import BlenderClosingDialog
from bqt.qt_core import QEvent, QObject, QRect, QSettings, QTimer, QCloseEvent, QIcon, QWindow, QApplication, QWidget, QMainWindow
import bpy
import bqt.manager
logger = logging.getLogger("bqt")


ORGANISATION = "Tech-Artists.org"
APP = "Blender Qt"
WINDOW_TITLE = "Blender Qt"
WINDOW_GROUP_NAME = "MainWindow"
GEOMETRY = "Geometry"
MAXIMIZED = "IsMaximized"
FULL_SCREEN = "IsFullScreen"
FOCUS_FRAMERATE = 15


class BlenderApplication(QApplication):
    """
    Base Implementation for QT Blender Window Container
    """

    def __init__(self, *args, **kwargs):
        __metaclass__ = ABCMeta
        super().__init__(*args, **kwargs)

        logger.debug("initializing BlenderApplication")

        self._active_window_hwnd = 0

        # QApplication.setWindowIcon(self._get_application_icon())

        # Blender Window
        self.window_container: QWidget = None
        self._hwnd = None
        if os.getenv("BQT_DISABLE_WRAP") != "1":
            logger.debug("wrapping enabled, getting blender hwnd")
            self._hwnd = self._get_blender_hwnd()
        else:
            logger.debug("wrapping disabled, not getting blender hwnd")
        failed_to_get_handle = self._hwnd is None
        if failed_to_get_handle:
            logger.warning("failed to get blender hwnd, creating new window")
            self._blender_window = QWindow()
            self.blender_widget = QWidget.createWindowContainer(self._blender_window)
        else:
            logger.debug(f"successfully got blender hwnd '{self._hwnd}', wrapping window in QMainWindow")
            self.blender_widget = QMainWindow()
            self.blender_widget.setWindowTitle(WINDOW_TITLE)
            self._blender_window = QWindow.fromWinId(self._hwnd)  # also sets flag to Qt.ForeignWindow
            self.window_container = QMainWindow.createWindowContainer(self._blender_window)
            self.blender_widget.setCentralWidget(self.window_container)

            self._set_window_geometry()
            self.blender_widget.show()
            logger.debug("hooking up _on_focus_object_changed")
            self.focusObjectChanged.connect(self._on_focus_object_changed)

        # hookup event loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_update)
        tick = int(1000 / FOCUS_FRAMERATE)  # tick 1000 / frames per second
        self.timer.start(tick)

        logger.debug("successfully initialized BlenderApplication")

    def on_update(self):
        """qt event loop"""
        # we only need foreground managing if blender is not wrapped
        if os.getenv("BQT_DISABLE_WRAP") == "1" and os.getenv("BQT_MANAGE_FOREGROUND", "1") == "1" and self.blender_focus_toggled():
            logger.debug("foreground window changed, managing")
            bqt.manager._blender_window_change(self._active_window_hwnd)

        if os.getenv("BQT_AUTO_ADD", "1") == "1":
            bqt.manager.parent_orphan_widgets(exclude=[self.blender_widget, self._blender_window, self.window_container])  # auto parent any orphaned widgets

    def blender_focus_toggled(self):
        """returns true the first frame the blender window is focussed or unfoccused"""
        current_active_hwnd = self._get_active_window_handle()
        handle_changed = self._active_window_hwnd != current_active_hwnd
        if not handle_changed:
            self._active_window_hwnd = current_active_hwnd
            return False
        else:
            # we toggled between 2 windows, but we only care if we toggled in or out of blender
            non_blender_toggle = self._active_window_hwnd == 0 or current_active_hwnd == 0
            self._active_window_hwnd = current_active_hwnd
            return non_blender_toggle


    @staticmethod
    def _get_active_window_handle():
        # override this method to get the active window handle
        return 0

    @staticmethod
    def _focus_window():
        pass

    @abstractstaticmethod
    def _get_blender_hwnd() -> int:
        """Get the handler window ID for the blender application window"""
        return -1

    @staticmethod
    def _get_application_icon() -> QIcon:
        """
        This finds the running blender process, extracts the blender icon from the blender.exe file on disk and saves it to the user's temp folder.
        It then creates a QIcon with that data and returns it.

        Returns QIcon: Application Icon
        """
        pass

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


    def notify(self, receiver: QObject, event: QEvent) -> bool:
        """
        Args:
            receiver: Object to receive event
            event: Event

        Returns: bool
        """
        # todo believe this func sometimes freezes blender, ctrl-c keyboard interrupt in console shows this func as the culprit

        if isinstance(event, QCloseEvent) and receiver in (self.blender_widget, self._blender_window):
            # catch the close event when clicking close on the qt window,
            # ignore the event, and ask user if they want to close blender if unsaved changes.
            event.ignore()

            self.store_window_geometry()  # save qt window geometry, to restore on next launch

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
