"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
from __future__ import annotations

import os
import logging
from pathlib import Path
from abc import abstractmethod, abstractstaticmethod, ABCMeta

from PySide6.QtCore import QEvent, QObject, QRect, QSettings, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtGui import QCloseEvent, QIcon, QWindow
import bpy
from bpy.app.handlers import persistent

from bqt.ui.quit_dialogue import BlenderClosingDialog, shutdown_blender_with_save_dialogue
import bqt.manager
import bqt.utils

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

    def __init__(self, *args, **kwargs) -> None:
        __metaclass__ = ABCMeta
        super().__init__(*args, **kwargs)

        logger.debug("initializing BlenderApplication")

        self._active_window_hwnd = 0

        # QApplication.setWindowIcon(self._get_application_icon())

        # Blender Window
        self.window_container: QWidget | None = None
        self._hwnd = None
        if os.getenv("BQT_DISABLE_WRAP") != "1":
            logger.debug("wrapping enabled, getting blender hwnd")
            self._hwnd = self._get_blender_hwnd()
        else:
            logger.debug("wrapping disabled, not getting blender hwnd")

        if self._hwnd is None:  # Failed to get handle
            logger.warning("failed to get blender hwnd, creating new window")
            self._blender_window: QWindow = QWindow()
            self.blender_widget: QWidget = QWidget.createWindowContainer(self._blender_window)
        else:
            logger.debug(f"successfully got blender hwnd '{self._hwnd}', wrapping window in QMainWindow")
            self.blender_widget: QMainWindow = QMainWindow()
            self.blender_widget.setWindowTitle(WINDOW_TITLE)
            self._blender_window: QWindow = QWindow.fromWinId(self._hwnd)  # also sets flag to Qt.ForeignWindow
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

    @staticmethod
    def _title(check_dirty: bool = True) -> str:
        # Standard title is like "Blender Qt 5.10"
        title = f"{WINDOW_TITLE} {bpy.app.version_string}"
        if not bpy.data.is_saved:
            # This happens for new unsaved files.
            title = f"(Unsaved) - {title}"
        else:
            # Add the current file path to the name
            f = Path(bpy.data.filepath)
            title = f"{f.stem} [{f.as_posix()}] - {title}"
        if check_dirty and bpy.data.is_dirty:
            # add dirty indicator
            title = f"* {title}"
        return title

    @persistent
    def update_window_title(self, *_) -> None:
        title = self._title()
        self.blender_widget.setWindowTitle(title)

    @persistent
    def update_window_title_post_save(self, *_) -> None:
        # It seems like the `is_dirty` flag is clear AFTER the post save handler.
        # This is only used in the post save, it shouldn't have unsaved changes.
        title = self._title(check_dirty=False)
        self.blender_widget.setWindowTitle(title)

    def on_update(self) -> None:
        """qt event loop"""
        # we only need foreground managing if blender is not wrapped
        if os.getenv("BQT_DISABLE_WRAP") == "1" and os.getenv("BQT_MANAGE_FOREGROUND", "1") == "1" and self.blender_focus_toggled():
            logger.debug("foreground window changed, managing")
            bqt.manager._blender_window_change(self._active_window_hwnd)

        if os.getenv("BQT_AUTO_ADD", "1") == "1":
            bqt.manager.parent_orphan_widgets(exclude=[self.blender_widget, self._blender_window, self.window_container])  # auto parent any orphaned widgets

    def blender_focus_toggled(self) -> bool:
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
    def _get_active_window_handle() -> int:
        # override this method to get the active window handle
        return 0

    @staticmethod
    def _focus_window(hwnd: int) -> None:
        pass

    @abstractstaticmethod
    def _get_blender_hwnd() -> int | None:
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
        Get the window geometry from the Blender window before it was wrapped in a QWidgetContainer.
        Blender reports coordinates in physical pixels; this method converts them to Qt logical pixels.
        Returns QRect(x, y, width, height) in Qt logical pixels.
        """
        window = bqt.utils.main_blender_window()
        width_phys, height_phys = window.width, window.height
        x_phys = window.x
        y_blender_phys = window.y  # blender y relative from bottom of screen

        # Convert physical pixels to logical pixels using the screen's DPI scale
        screen = self._screen_for_physical_x(x_phys) or self.primaryScreen()
        dpr = screen.devicePixelRatio()

        x = int(x_phys / dpr)
        width = int(width_phys / dpr)
        height = int(height_phys / dpr)
        y_blender = int(y_blender_phys / dpr)

        # Convert y from bottom-relative to top-relative
        screen_rect = screen.availableGeometry()
        y = screen_rect.height() + screen_rect.y() - y_blender - height

        return QRect(x, y, width, height)

    def _screen_for_physical_x(self, x_phys: int):
        """Find the screen whose physical x range contains x_phys."""
        for screen in self.screens():
            geo = screen.geometry()
            dpr = screen.devicePixelRatio()
            phys_left = int(geo.x() * dpr)
            phys_right = int((geo.x() + geo.width()) * dpr)
            if phys_left <= x_phys < phys_right:
                return screen
        return None

    def _is_geometry_visible(self, geometry: QRect) -> bool:
        """Check if at least a reasonable portion of the window is visible on any screen."""
        min_visible = 100  # pixels - at least this much must be on-screen
        for screen in self.screens():
            intersection = screen.availableGeometry().intersected(geometry)
            if intersection.width() >= min_visible and intersection.height() >= min_visible:
                return True
        return False

    def _is_native_window_maximized(self) -> bool:
        """Check if the native Blender window is maximized by checking
        whether the window covers most of a screen's physical area."""
        window = bqt.utils.main_blender_window()
        w_phys, h_phys = window.width, window.height
        for screen in self.screens():
            dpr = screen.devicePixelRatio()
            screen_w = int(screen.geometry().width() * dpr)
            screen_h = int(screen.geometry().height() * dpr)
            coverage = (w_phys * h_phys) / max(screen_w * screen_h, 1)
            if coverage >= 0.90:
                return True

        return False

    def _default_normal_geometry(self) -> QRect:
        """Return a sensible 80%-of-screen centered geometry for the restore/normal state."""
        screen_rect = self.primaryScreen().availableGeometry()
        w = int(screen_rect.width() * 0.8)
        h = int(screen_rect.height() * 0.8)
        x = screen_rect.x() + (screen_rect.width() - w) // 2
        y = screen_rect.y() + (screen_rect.height() - h) // 2
        return QRect(x, y, w, h)

    def _show_maximized_with_normal_geometry(self) -> None:
        """Maximize the window, but first set a sensible normal geometry
        so that restoring from maximized gives a usable window size."""
        self.blender_widget.setGeometry(self._default_normal_geometry())
        self.blender_widget.showMaximized()

    def _set_window_geometry(self) -> None:
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
            self._show_maximized_with_normal_geometry()
            self.blender_widget.showFullScreen()
            return

        # Check saved maximized flag, or detect if native Blender window is maximized
        if maximized or (saved_geometry is None and self._is_native_window_maximized()):
            self._show_maximized_with_normal_geometry()
            return

        unwrapped_geometry = self._unwrapped_window_geometry()
        geometry = saved_geometry or unwrapped_geometry

        # Validate that the geometry is visible on at least one screen.
        # If not (e.g. monitor was disconnected, DPI changed), fall back to maximized.
        if self._is_geometry_visible(geometry):
            self.blender_widget.setGeometry(geometry)
        else:
            self._show_maximized_with_normal_geometry()


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
                shutdown_blender_with_save_dialogue()
            else:
                closing_dialog = BlenderClosingDialog(self.blender_widget)
                closing_dialog.execute()

            return False

        return super().notify(receiver, event)

    def store_window_geometry(self) -> None:
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
