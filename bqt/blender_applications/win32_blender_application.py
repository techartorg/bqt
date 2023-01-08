"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
import bpy
from PySide6.QtCore import QObject
from .blender_application import BlenderApplication
import ctypes
import os
from ctypes import wintypes
from collections import namedtuple


def get_process_hwnds():
    # https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    def check_zero(result, func, args):
        if not result:
            err = ctypes.get_last_error()
            if err:
                raise ctypes.WinError(err)
        return args

    if not hasattr(wintypes, "LPDWORD"):  # PY2
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

    WindowInfo = namedtuple("WindowInfo", "title hwnd")

    WNDENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND,  # _In_ hWnd
        wintypes.LPARAM,
    )  # _In_ lParam

    user32.EnumWindows.errcheck = check_zero
    user32.EnumWindows.argtypes = (
        WNDENUMPROC,  # _In_ lpEnumFunc
        wintypes.LPARAM,
    )  # _In_ lParam

    user32.IsWindowVisible.argtypes = (wintypes.HWND,)  # _In_ hWnd

    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetWindowThreadProcessId.argtypes = (
        wintypes.HWND,  # _In_      hWnd
        wintypes.LPDWORD,
    )  # _Out_opt_ lpdwProcessId

    user32.GetWindowTextLengthW.errcheck = check_zero
    user32.GetWindowTextLengthW.argtypes = (wintypes.HWND,)  # _In_ hWnd

    user32.GetWindowTextW.errcheck = check_zero
    user32.GetWindowTextW.argtypes = (
        wintypes.HWND,  # _In_  hWnd
        wintypes.LPWSTR,  # _Out_ lpString
        ctypes.c_int,
    )  # _In_  nMaxCount

    def list_windows():
        """Return a sorted list of visible windows."""
        result = []

        @WNDENUMPROC
        def enum_proc(hWnd, lParam):
            if user32.IsWindowVisible(hWnd):
                pid = wintypes.DWORD()
                tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
                length = user32.GetWindowTextLengthW(hWnd) + 1
                title = ctypes.create_unicode_buffer(length)
                user32.GetWindowTextW(hWnd, title, length)
                current_pid = os.getpid()
                if pid.value == current_pid:
                    result.append(WindowInfo(title.value, hWnd))
            return True

        user32.EnumWindows(enum_proc, 0)
        return sorted(result)

    return list_windows()


def get_first_blender_window():
    process_windows = get_process_hwnds()
    return process_windows[0].hwnd


class Win32BlenderApplication(BlenderApplication):
    """
    Windows implementation of BlenderApplication
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_application_hwnd() -> int:
        """
        This finds the blender application window and collects the
        handler window ID

        Returns int: Handler Window ID
        """

        hwnd = get_first_blender_window()
        return hwnd

    def _on_focus_object_changed(self, focus_object: QObject):
        """
        Args:
            QObject focus_object: Object to track focus change
        """
        if focus_object is self.blender_widget:
            ctypes.windll.user32.SetFocus(self._hwnd)
            with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
                bpy.ops.bqt.return_focus("INVOKE_DEFAULT")


__all__ = ["Win32BlenderApplication"]
