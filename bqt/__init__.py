"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import atexit
import os
import sys

import bpy

from PySide2.QtWidgets import QApplication

from .blender_applications import BlenderApplication

# GLOBALS #
TICK = 1.0 / float(os.getenv("BQT_TICK_RATE", "30"))


class QOperator(bpy.types.Operator):
    """
    QOperator is a subclass of the Blender `bpy.types.Operator`
    It instantiates the application if one does not exist already
    """
    bl_idname = "qoperator.global_app"
    bl_label = "Global QApplication"

    def __init__(self):
        super().__init__()
        self._qapp = None


    def execute(self, context) -> set:
        """
        Args:
            context: Blender Context
        Returns:
            set
        """
        self._qapp = instantiate_application()
        return {'PASS_THROUGH'}


# CORE FUNCTIONS #
def instantiate_application() -> BlenderApplication:
    """
    Create an instance of Blender Application
    Returns BlenderApplication: Application Instance
    """
    app = QApplication.instance()
    if not app:
        app = load_os_module()
        bpy.app.timers.register(on_update, persistent=True)

    return app


def load_os_module() -> object:
    """
    Loads the correct OS platform Application Class
    Returns: Instance of BlenderApplication
    """
    operating_system = sys.platform
    if operating_system == 'darwin':
        from .blender_applications.darwin_blender_application import DarwinBlenderApplication
        return DarwinBlenderApplication()
    if operating_system in ['linux', 'linux2']:
        # TODO: LINUX module
        pass
    elif operating_system == 'win32':
        from .blender_applications.win32_blender_application import Win32BlenderApplication
        return Win32BlenderApplication()


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
        app.store_window_geometry()
        app.quit()


atexit.register(on_exit)


if __name__ == '__main__':
    try:
        unregister()
    except (ValueError, TypeError) as e:
        print(f"Failed to unregister QOperator: {e}")

    register()