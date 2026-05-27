"""
Forward WM_ACTIVATE from bqt's Qt top-level down to the wrapped GHOST HWND.

When bqt reparents main Blender's GHOST HWND as a child of a Qt container
window, Windows stops delivering WM_ACTIVATE to the GHOST HWND (only
top-level windows get it). Blender's GHOST tracks its internal "active
window" via WM_ACTIVATE, so without this forward GHOST's view of which
Blender window is active gets stuck on whatever secondary GHOST window
was opened last.
This for example causes modifier keys in the main viewport to stop
working if additional Blender windows have been opened since.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Callable

from PySide6.QtCore import QAbstractNativeEventFilter
from PySide6.QtWidgets import QApplication

WM_ACTIVATE = 0x0006
_WINDOWS_MSG_TYPE = b"windows_generic_MSG"
_user32 = ctypes.windll.user32


class _MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt_x", wintypes.LONG),
        ("pt_y", wintypes.LONG),
    ]


def _is_ancestor_of(ancestor: int, descendant: int) -> bool:
    if not ancestor or not descendant:
        return False
    cur = _user32.GetParent(descendant)
    while cur:
        if cur == ancestor:
            return True
        cur = _user32.GetParent(cur)
    return False


class _ActivateForwarder(QAbstractNativeEventFilter):
    """Re-sends WM_ACTIVATE from any Qt top-level ancestor of the wrapped
    GHOST HWND down to GHOST itself."""

    def __init__(self, blender_hwnd_getter: Callable[[], int]):
        super().__init__()
        self._get_hwnd = blender_hwnd_getter

    def nativeEventFilter(self, event_type, message):
        if event_type != _WINDOWS_MSG_TYPE:
            return False, 0
        msg = _MSG.from_address(int(message))
        if msg.message != WM_ACTIVATE:
            return False, 0
        ghost_hwnd = self._get_hwnd() or 0
        if ghost_hwnd and _is_ancestor_of(msg.hwnd, ghost_hwnd):
            _user32.SendMessageW(ghost_hwnd, WM_ACTIVATE, msg.wParam, msg.lParam)
        return False, 0


_filter: _ActivateForwarder | None = None


def install(app: QApplication, blender_hwnd_getter: Callable[[], int]) -> None:
    """Install the WM_ACTIVATE forwarder. The getter is called per event so
    the HWND isn't captured stale if bqt ever re-wraps."""
    global _filter
    if _filter is not None:
        return
    _filter = _ActivateForwarder(blender_hwnd_getter)
    app.installNativeEventFilter(_filter)
