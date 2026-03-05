from typing import Callable
import traceback

import bpy


def try_except(func) -> Callable:
    """
    Prevent blender from crashing on an exception.
    Decorator to wrap a function in try except and print the traceback
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()

    return wrapper


def main_blender_window() -> bpy.types.Window:
    """
    Sometimes windows[0] returns the settings screen instead of the main window
    """
    windows = bpy.context.window_manager.windows
    for window in windows:
        if window.parent is None:
            return window
        
def context_window(func) -> Callable:
    """
    Support running operators from QT (ex. on button click).
    Decorator to override the context window for a function,
    """

    def wrapper(*args, **kwargs):
        with bpy.context.temp_override(window=main_blender_window()):
            return func(*args, **kwargs)

    return wrapper

