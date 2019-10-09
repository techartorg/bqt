# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
import atexit
import os
import sys
import types

import win32gui

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QWindow, QKeyEvent, QCloseEvent
from PySide2.QtCore import Qt
import bpy
from bpy.app.handlers import persistent

TICK = 1.0 / float(os.getenv("BQT_TICK_RATE", '30'))


class BlenderApplication(QApplication):

    def __init__(self, argv=None):
        argv = [] if argv is None else argv
        super().__init__(argv)
        self.should_close = False
        self._hwnd = win32gui.FindWindow(None, 'blender')
        self._blender_window = QWindow.fromWinId(self._hwnd)
        self.blender_widget = QWidget.createWindowContainer(self._blender_window)
        self.blender_widget.show()
        self.focusObjectChanged.connect(self._on_focus_object_changed)

    def notify(self, receiver: QObject, event: QEvent):
        if isinstance(event, QCloseEvent) and receiver in (self.blender_widget, self._blender_window):
            event.ignore()
            self.should_close = True
            return False
        return super().notify(receiver, event)

    def _on_focus_object_changed(self, focus_object: QObject):
        if focus_object is self.blender_widget:
            win32gui.SetFocus(self._hwnd)


class QOperator(bpy.types.Operator):
    """
    QOperator is a subclass of the Blender `bpy.types.Operator`
    It instantiates the application if one does not exist already
    """

    bl_idname = "qoperator.global_app"
    bl_label = "Global QApplication"

    def execute(self, context):
        self.__qapp = instantiate_application()
        return {'PASS_THROUGH'}


def instantiate_application():
    app = QApplication.instance()
    if not app:
        app = BlenderApplication(sys.argv)
        bpy.app.timers.register(on_update, persistent=True)
    return app


def on_update():
    app = QApplication.instance()
    if app.should_close:
        bpy.ops.wm.quit_blender({'window': bpy.context.window_manager.windows[0]}, 'INVOKE_DEFAULT')
    return TICK


@persistent
def create_global_app(*args):
    if 'startup' in __file__ and not os.getenv("BQT_DISABLE_STARTUP"):
        bpy.ops.qoperator.global_app()


def register():
    bpy.utils.register_class(QOperator)
    if not create_global_app in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(create_global_app)


def unregister():
    bpy.utils.unregister_class(QOperator)
    if create_global_app in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(create_global_app)


def onexit():
    app = QApplication.instance()
    if app:
        app.quit()


atexit.register(onexit)

if __name__ == '__main__':
    try:
        unregister()
    except Exception as e:
        print("Failed to unregister QOperator: {}".format(e))

    register()
