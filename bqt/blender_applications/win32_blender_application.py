"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from __future__ import annotations

import ctypes
import os
from collections import namedtuple
from ctypes import wintypes

from PySide6.QtCore import QObject

from bqt import win32_native_filter

from .blender_application import BlenderApplication

user32 = ctypes.windll.user32


def get_class_name(hwnd):
    # returns "GHOST_WindowClass" for Blender and BlenderWindows (e.g. Preferences),
    # ref: https://github.com/blender/blender/blob/v5.1.1/intern/ghost/intern/GHOST_WindowWin32.cc#L46
    # returns "PseudoConsoleWindow" for the terminal window
    buf_len = 256
    buf = ctypes.create_unicode_buffer(buf_len)
    user32.GetClassNameW(hwnd, buf, buf_len)
    return buf.value


def get_process_hwnds():
    # https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python

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

                # get title
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


def get_blender_window() -> None | int:
    process_windows = get_process_hwnds()
    if not process_windows:
        return None

    # GHOST creates each Blender viewport/preferences window as its own
    # top-level Win32 window, so filtering on GetParent()==0 alone is ambiguous
    # when multiple are open. Require class "GHOST_WindowClass" and confirm the
    # window is its own root via GetAncestor(GA_ROOT).
    GA_ROOT = 2
    for win in process_windows:
        if get_class_name(win.hwnd) != "GHOST_WindowClass":
            continue
        if ctypes.windll.user32.GetAncestor(win.hwnd, GA_ROOT) != win.hwnd:
            continue
        return win.hwnd

    return process_windows[0].hwnd


class Win32BlenderApplication(BlenderApplication):
    """
    Windows implementation of BlenderApplication
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        win32_native_filter.install(self, lambda: self._hwnd or 0)

    @staticmethod
    def _get_blender_hwnd() -> int | None:
        """Get the handler window ID for the blender application window"""
        hwnd = get_blender_window()
        return hwnd

    def _on_focus_object_changed(self, focus_object: QObject) -> None:
        """
        Args:
            QObject focus_object: Object to track focus change
        """
        if focus_object is self.blender_widget:
            ctypes.windll.user32.SetFocus(self._hwnd)

    @staticmethod
    def _get_active_window_handle() -> int:
        """
        Get the handle from the window that's currently in focus.
        Returns 0 for active windows not managed by Blender
        """
        # note that negative values are also possible
        return user32.GetActiveWindow()

    @staticmethod
    def _focus_window(hwnd: int) -> None:
        """Focus the window with the given handle."""
        user32.SetForegroundWindow(hwnd)
        # user32.SetFocus(hwnd)
