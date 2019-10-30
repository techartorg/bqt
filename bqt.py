"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import atexit
import os
from pathlib import Path
import sys

import bpy

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QWindow
from PySide2.QtCore import QEvent, QObject


# GLOBALS ###
STYLESHEET_FILEPATH = Path(__file__).parent / 'blender_stylesheet.qss'
TICK = 1.0 / float(os.getenv("BQT_TICK_RATE", "30"))


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
        self.os_module.notify(receiver, event)

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
        self.os_module.__set_window_geometry()

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

        Returns: None
        """
        self.os_module.__store_window_geometry()

    @staticmethod
    def load_os_module():
        """
        Loads the correct OS platform Application Class

        Returns: Instance of BlenderApplication

        """
        operating_system = sys.platform
        if operating_system == 'darwin':
            # TODO: MACOS module
            pass
        if operating_system in ['linux', 'linux2']:
            # TODO: LINUX module
            pass
        elif operating_system == 'win32':
            from blender_applications import Win32BlenderApplication
            return Win32BlenderApplication


class QOperator(bpy.types.Operator):
    """
    QOperator is a subclass of the Blender `bpy.types.Operator`
    It instantiates the application if one does not exist already
    """
    bl_idname = "qoperator.global_app"
    bl_label = "Global QApplication"

    def __init__(self):
        super().__init__()
        self.__qapp = None

    def execute(self, context):
        """

        Args:
            context: Blender Context

        Returns:

        """
        self.__qapp = instantiate_application()
        return {'PASS_THROUGH'}


# CORE FUNCTIONS ###

def instantiate_application() -> BlenderApplication:
    """
    Create an instance of Blender Application

    Returns BlenderApplication: Application Instance

    """
    app = QApplication.instance()
    if not app:
        app = BlenderApplication(sys.argv)
        bpy.app.timers.register(on_update, persistent=True)

    return app


def on_update() -> float:
    """
    Checks per Blender timer tick to verify if application should close

    Returns: Tick Rate

    """
    app = QApplication.instance()
    if app.should_close:
        bpy.ops.wm.quit_blender({'window': bpy.context.window_manager.windows[0]}, 'INVOKE_DEFAULT')

    return TICK


@bpy.app.handlers.persistent
def create_global_app(*_args):
    """
    Create global application
    Args:
        *_args:

    Returns:

    """
    if 'startup' in __file__ and not os.getenv('BQT_DISABLE_STARTUP'):
        bpy.ops.qoperator.global_app()


def register():
    """
    Register Blender Operator classes

    Returns: None

    """
    bpy.utils.register_class(QOperator)
    if create_global_app not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(create_global_app)


def unregister():
    """
    Unregister Blender Operator classes

    Returns: None

    """
    bpy.utils.unregister_class(QOperator)
    if create_global_app in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(create_global_app)


def on_exit():
    """
    Close BlenderApplication instance on exit

    Returns: None

    """
    app = QApplication.instance()
    if app:
        app.quit()


atexit.register(on_exit)


if __name__ == '__main__':
    try:
        unregister()
    except (ValueError, TypeError) as e:
        print(f"Failed to unregister QOperator: {e}")
