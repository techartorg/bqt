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


def apply_bpy_app_patches():
    """Apply all bpy.app module patches. Order matters!"""
    # First patch sys.modules
    for module_name in _BPY_APP_MODULES_TO_PATCH:
        _patch_bpy_module_in_sys_modules(module_name)

    # Then fix existing modules
    for module_name in _BPY_APP_MODULES_TO_PATCH:
        _fix_existing_bpy_module(module_name)
