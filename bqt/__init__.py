"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# CRITICAL: Fix bpy.app submodules BEFORE importing any Qt/PySide modules
# This prevents Shiboken from failing when it tries to introspect bpy.app.translations/handlers
# See: https://github.com/techartorg/bqt/issues/127
import sys

# Modules that need patching for Shiboken compatibility
_BPY_APP_MODULES_TO_PATCH = ['translations', 'handlers']


def _create_bpy_app_wrapper(original, module_name):
    """Create a compatibility wrapper for bpy.app submodules.

    Args:
        original: The original bpy.app submodule object
        module_name: Name of the module (e.g., 'translations', 'handlers')
    """
    class BpyAppModuleWrapper:
        __slots__ = ('_orig',)

        def __init__(self, orig):
            object.__setattr__(self, '_orig', orig)

        def __getattr__(self, name):
            # Provide missing attributes that Shiboken expects
            if name == '__name__':
                return 'bpy.app.{}'.format(module_name)
            elif name == '__module__':
                return 'bpy.app'
            elif name == '__qualname__':
                return module_name
            elif name == '__ne__':
                return lambda self, other: not self.__eq__(other)
            elif name == '__doc__':
                return 'Blender {} compatibility wrapper'.format(module_name)
            return getattr(object.__getattribute__(self, '_orig'), name)

        def __setattr__(self, name, value):
            if name == '_orig':
                object.__setattr__(self, name, value)
            else:
                setattr(object.__getattribute__(self, '_orig'), name, value)

        def __dir__(self):
            orig = object.__getattribute__(self, '_orig')
            orig_attrs = dir(orig) if hasattr(orig, '__dir__') else []
            extra_attrs = ['__name__', '__module__', '__qualname__', '__ne__', '__doc__']
            return list(set(orig_attrs + extra_attrs))

        def __repr__(self):
            return '<BpyAppModuleWrapper for bpy.app.{}>'.format(module_name)

    return BpyAppModuleWrapper(original)


def _patch_bpy_module_in_sys_modules(module_name):
    """Patch bpy.app.{module_name} in sys.modules if it exists and needs patching."""
    full_name = "bpy.app.{}".format(module_name)
    if full_name not in sys.modules:
        return False

    module = sys.modules[full_name]
    required_attrs = ['__name__', '__module__', '__qualname__']

    # Only patch if missing required attributes
    if all(hasattr(module, attr) for attr in required_attrs):
        return False

    wrapped = _create_bpy_app_wrapper(module, module_name)
    sys.modules[full_name] = wrapped
    return True


def _fix_existing_bpy_module(module_name):
    """Fix bpy.app.{module_name} if it already exists and needs patching."""
    import bpy
    if not hasattr(bpy.app, module_name):
        return False

    module = getattr(bpy.app, module_name)
    required_attrs = ['__name__', '__module__', '__qualname__']

    # Only fix if missing required attributes
    if all(hasattr(module, attr) for attr in required_attrs):
        return False

    # Try direct attribute setting first
    attrs_to_add = {
        '__name__': 'bpy.app.{}'.format(module_name),
        '__module__': 'bpy.app',
        '__qualname__': module_name,
    }

    try:
        for attr_name, attr_value in attrs_to_add.items():
            if not hasattr(module, attr_name):
                setattr(module, attr_name, attr_value)
        return True
    except (AttributeError, TypeError):
        # If direct setting fails, use wrapper
        wrapped = _create_bpy_app_wrapper(module, module_name)
        setattr(bpy.app, module_name, wrapped)
        return True


def _apply_bpy_app_patches():
    """Apply all bpy.app module patches. Order matters!"""
    # First patch sys.modules
    for module_name in _BPY_APP_MODULES_TO_PATCH:
        _patch_bpy_module_in_sys_modules(module_name)

    # Then fix existing modules
    for module_name in _BPY_APP_MODULES_TO_PATCH:
        _fix_existing_bpy_module(module_name)


# Apply patches immediately before any Qt/PySide imports
_apply_bpy_app_patches()

import os
from pathlib import Path

# add to sys path so we can import bqt
current_dir = str(Path(__file__).parent.parent)
if current_dir not in sys.path:
    sys.path.append(current_dir)


import bqt
import bqt.focus
import bqt.manager
import bpy
from bqt.qt_core import QtCore, QApplication
import logging

logger = logging.getLogger("bqt")
add = bqt.manager.register


def _apply_stylesheet():
    """Styles the QApplication"""
    try:
        import blender_stylesheet
        blender_stylesheet.setup()
    except ImportError:
        logger.warning("blender-qt-stylesheet not found, using default style")


def _enable_dpi_scale():
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)


def _instantiate_q_application() -> "bqt.blender_applications.BlenderApplication":
    _enable_dpi_scale()
    app = _load_os_module()
    _apply_stylesheet()
    return app


def _load_os_module() -> "bqt.blender_applications.BlenderApplication":
    """Loads the correct OS platform Application Class"""
    operating_system = sys.platform
    logger.debug(f"loading OS module for '{operating_system}'")
    if operating_system == "darwin":
        from .blender_applications.darwin_blender_application import DarwinBlenderApplication

        return DarwinBlenderApplication(sys.argv)

    elif operating_system in ["linux", "linux2"]:
        raise NotImplementedError("Linux is not supported yet")
        # TODO: LINUX module
        pass

    elif operating_system == "win32":
        from .blender_applications.win32_blender_application import Win32BlenderApplication

        return Win32BlenderApplication(sys.argv + ['-platform', 'windows:darkmode=2'])

    else:
        raise OSError(f"OS module for '{operating_system}' not found")


@bpy.app.handlers.persistent
def _create_global_app():
    """
    Create a global QApplication instance, that's maintained between Blender sessions.
    Runs after Blender finished startup.
    """
    qapp = _instantiate_q_application()
    # save a reference to the C++ window in a global var, to prevent the parent being garbage collected
    # for some reason this works here, but not in the blender_applications init as a class attribute (self),
    # and saving it in a global in blender_applications.py causes blender to crash on startup
    global parent_window
    parent_window = qapp._blender_window.parent()


def setup_logger():
    """setup logger, using BQT_LOG_LEVEL env var"""
    log_level_name = os.getenv("BQT_LOG_LEVEL", -1)
    if log_level_name == -1:
        logger.debug("BQT_LOG_LEVEL not set, using default 'WARNING'")
        log_level_name = "WARNING"
    if log_level_name not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        logger.warning("BQT_LOG_LEVEL is set to invalid value '{}', using default 'WARNING'".format(log_level_name))
        log_level_name = "WARNING"
    # print(f"BQT_LOG_LEVEL is set to '{log_level_name}'")
    log_level = logging.getLevelName(log_level_name)
    logger.setLevel(log_level)
    # encoding parameter was added in Python 3.9, use conditional for Blender 2.83 compatibility
    if sys.version_info >= (3, 9):
        logging.basicConfig(encoding='utf-8')
    else:
        logging.basicConfig()


def register():
    """
    Runs on enabling the add-on.
    setup bqt, wrap blender in qt, register operators
    """
    setup_logger()
    logger.debug("registering bqt add-on")
    # hacky way to check if we already are waiting on bqt setup, or bqt is already setup
    if QApplication.instance():
        logger.warning("QApplication already exists, skipping bqt registration")
        return
    if os.getenv("BQT_DISABLE_STARTUP", 0) == "1":
        logger.warning("BQT_DISABLE_STARTUP is set, skipping bqt registration")
        return
    _create_global_app()


def unregister():
    """
    Runs on disabling the add-on.
    """
    # todo, as long as blender is wrapped in qt, unregistering operator & callback will cause issues,
    #  for now we just return since unregister should not be called partially
    logger.debug("unregistering bqt add-on")
    logger.warning("unregistering bqt is not supported yet, skipping")
    # if not os.getenv("BQT_DISABLE_WRAP", 0) == "1":
    #     bpy.utils.unregister_class(bqt.focus.QFocusOperator)
