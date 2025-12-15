from __future__ import annotations
import traceback
from typing import Callable

import bpy

def try_except(func: Callable) -> Callable:
    """
    Prevent blender from crashing on an exception.
    Decorator to wrap a function in try except and print the traceback
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            traceback.print_exc()

    return wrapper


def context_window(func: Callable) -> Callable:
    """
    Support running operators from QT (ex. on button click).
    Decorator to override the context window for a function,
    """

    def wrapper(*args, **kwargs):
        with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
            return func(*args, **kwargs)

    return wrapper
