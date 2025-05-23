"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# CRITICAL: Fix bpy.app.translations BEFORE importing any Qt/PySide modules
# This prevents Shiboken from failing when it tries to introspect bpy.app.translations
import sys


def _create_translations_wrapper(original):
    """Create a compatibility wrapper for bpy.app.translations"""
    class TranslationsWrapper:
        def __init__(self, orig):
            self._orig = orig

        def __getattr__(self, name):
            # Provide missing attributes that Shiboken expects
            if name == '__name__':
                return 'bpy.app.translations'
            elif name == '__module__':
                return 'bpy.app'
            elif name == '__qualname__':
                return 'translations'
            elif name == '_ne_':
                return lambda x, y: x != y
            elif name == '__doc__':
                return 'Blender translations compatibility wrapper'
            else:
                return getattr(self._orig, name)

        def __setattr__(self, name, value):
            if name == '_orig':
                super().__setattr__(name, value)
            else:
                setattr(self._orig, name, value)

        def __dir__(self):
            orig_attrs = (dir(self._orig)
                          if hasattr(self._orig, '__dir__') else [])
            extra_attrs = ['__name__', '__module__', '__qualname__',
                           '_ne_', '__doc__']
            return list(set(orig_attrs + extra_attrs))

    return TranslationsWrapper(original)


def _patch_bpy_translations_in_sys_modules():
    """Directly patch bpy.app.translations in sys.modules if it exists"""
    try:
        # Check if bpy.app.translations is already in sys.modules
        if "bpy.app.translations" in sys.modules:
            translations = sys.modules["bpy.app.translations"]
            required_attrs = ['__name__', '__module__', '__qualname__', '_ne_']

            # Check if any required attributes are missing
            if any(not hasattr(translations, attr) for attr in required_attrs):
                try:
                    wrapped = _create_translations_wrapper(translations)
                    sys.modules["bpy.app.translations"] = wrapped
                    return True
                except Exception:
                    pass
        return False
    except Exception:
        return False


def _fix_existing_translations():
    """Fix bpy.app.translations if it already exists"""
    try:
        import bpy
        if not hasattr(bpy.app, 'translations'):
            return

        translations = bpy.app.translations
        required_attrs = ['__name__', '__module__', '__qualname__', '_ne_']

        # Check if any required attributes are missing
        if any(not hasattr(translations, attr) for attr in required_attrs):
            try:
                # Try direct attribute setting first
                attrs_to_add = {
                    '__name__': 'bpy.app.translations',
                    '__module__': 'bpy.app',
                    '__qualname__': 'translations',
                    '_ne_': lambda x, y: x != y,
                }

                for attr_name, attr_value in attrs_to_add.items():
                    if not hasattr(translations, attr_name):
                        setattr(translations, attr_name, attr_value)

            except (AttributeError, TypeError):
                # If direct setting fails, use wrapper
                try:
                    bpy.app.translations = _create_translations_wrapper(translations)
                except Exception:
                    pass

    except Exception:
        pass


# Apply patches immediately - order matters!
_patch_bpy_translations_in_sys_modules()  # Check sys.modules first
_fix_existing_translations()  # Fix existing translations if available

import bqt
import bqt.focus
import bqt.manager
import os
import sys
import bpy
from bqt.qt_core import QtCore, QApplication
import logging

logger = logging.getLogger("bqt")


bl_info = {
        "name": "PySide Qt wrapper (bqt)",
        "description": "Enable PySide QtWidgets in Blender",
        "author": "tech-artists.org",
        "version": (1, 4, 2),
        "blender": (2, 80, 0),
        # "location": "",
        # "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "https://github.com/techartorg/bqt/wiki",
        "tracker_url": "https://github.com/techartorg/bqt/issues",
        "support": "COMMUNITY",
        "category": "UI"
        }

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
        logger.warning(f"BQT_LOG_LEVEL is set to invalid value '{log_level_name}', using default 'WARNING'")
        log_level_name = "WARNING"
    # print(f"BQT_LOG_LEVEL is set to '{log_level_name}'")
    log_level = logging.getLevelName(log_level_name)
    logger.setLevel(log_level)
    logging.basicConfig(encoding='utf-8')


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
