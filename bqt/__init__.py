"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import sys
from pathlib import Path
import bpy
import shutil

bl_info = {
    "name": "bqt",
    "author": "tech-artists.org",
    "description": "PySide6 application loop utility",
    "blender": (3, 4, 0),
    "version": (2, 4, 1),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
}


def ShowMessageBox(message="", title="Message Box", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# - CHECK STARTUP
HERE = Path(__file__).parent
USER_PATH = Path(bpy.utils.resource_path("USER"))
STARTUP = USER_PATH / "scripts" / "startup" / "bqt_startup.py"


if not STARTUP.is_file():
    print("bqt: Startup file not found, installing...")
    shutil.copy(HERE / "data" / "bqt_startup.py", STARTUP)
    print(f"bqt: Installed to {STARTUP.as_posix()}")
    ShowMessageBox("Please restart blender", "bqt startup file installed")


from bqt import focus
import atexit
import os
import PySide6.QtCore as QtCore
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir

from .blender_applications import BlenderApplication

VERSION = "0.2.1"

# CORE FUNCTIONS #


def instantiate_application() -> BlenderApplication | QApplication:
    """
    Create an instance of Blender Application

    Returns BlenderApplication: Application Instance

    """
    # enable dpi scale, run before creating QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    image_directory = str(Path(__file__).parent / "images")
    QDir.addSearchPath("images", image_directory)
    return QApplication.instance() or load_os_module()


def load_os_module() -> object:
    """
    Loads the correct OS platform Application Class

    Returns: Instance of BlenderApplication

    """
    operating_system = sys.platform
    if operating_system == "darwin":
        from .blender_applications.darwin_blender_application import (
            DarwinBlenderApplication,
        )

        return DarwinBlenderApplication(sys.argv)
    if operating_system in ["linux", "linux2"]:
        # TODO: LINUX module
        pass
    elif operating_system == "win32":
        from .blender_applications.win32_blender_application import (
            Win32BlenderApplication,
        )

        return Win32BlenderApplication(sys.argv)


parent_window = None


@bpy.app.handlers.persistent
def create_global_app(dummy):
    """
    runs after blender finished startup
    """
    # global qapp
    qapp = instantiate_application()

    # save a reference to the C++ window in a global var, to prevent the parent being garbage collected
    # for some reason this works here, but not in the blender_applications init as a class attribute (self),
    # and saving it in a global in blender_applications.py causes blender to crash on startup
    global parent_window
    parent_window = qapp._blender_window.parent()

    # after blender is wrapped in QWindow,
    # remove the  handle so blender is not wrapped again when opening a new scene
    bpy.app.handlers.load_post.remove(create_global_app)


def register():
    """
    setup bqt, wrap blender in qt, register operators
    """

    if os.getenv("BQT_DISABLE_STARTUP", 0) == "1":
        return

    # only start focus operator if blender is wrapped
    if os.getenv("BQT_DISABLE_WRAP", 0) != "1":
        bpy.utils.register_class(focus.QFocusOperator)

    # append add_focus_handle before create_global_app,
    # else it doesn't run on blender startup
    # guessing that wrapping blender in QT interrupts load_post
    # resulting in the load_post handler not called on blender startup

    # use load_post since blender doesn't like data changed before scene is loaded,
    # wrap blender after first scene is loaded, the operator removes itself on first run
    if create_global_app not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(create_global_app)

    atexit.register(on_exit)


def unregister():
    """
    Unregister Blender Operator classes

    Returns: None

    """
    if os.getenv("BQT_DISABLE_WRAP", 0) != "1":
        bpy.utils.unregister_class(focus.QFocusOperator)
    if create_global_app in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(create_global_app)
    atexit.unregister(on_exit)


def on_exit():
    """Close BlenderApplication instance on exit"""
    if app := QApplication.instance():
        app.store_window_geometry()
        app.quit()
