"""
when alt tabbing in and out of blender, a bug happens when blender is wrapped in qt.
some keys stay stuck, e.g. alt or control, resulting in the user
not being able to use blender on refocus

this module fixes the bug by sending a key release event to the window
"""

import ctypes


def _detect_keyboard(hwnd=None):
    """
    force a release of 'stuck' keys
    """
    # if hwnd:
    #     ctypes.windll.user32.SetFocus(hwnd)
    #     ctypes.windll.user32.SetForegroundWindow(hwnd)

    # key codes from https://itecnote.com/tecnote/python-simulate-keydown/
    keycodes = [
        ("_ALT", 0x12),
        ("_CTRL", 0x11),
        ("_SHIFT", 0x10),
        ("VK_LWIN", 0x5B),
        ("VK_RWIN", 0x5C),
        ("OSKEY", 0x5B),  # dupe oskey, blender names it this
    ]

    # print("event.type", event.type, type(event.type))
    for name, code in keycodes:
        # todo this bug fix is not perfect yet, blender works better without this atm
        # # if the first key pressed is one of the following,
        # # don't simulate a key release, since it causes this bug:
        # # the first keypress on re-focus blender will be ignored, e.g. ctrl + v will just be v
        # if name in event.type:
        #     print("skipping:", name)
        #     continue

        # safely release all other keys that might be stuck down
        ctypes.windll.user32.keybd_event(code, 0, 2, 0)  # release key

    # todo, fix: blender occasionally still frozen input, despite having run the above code
    # but when we click the mouse, it starts working again
    # simulate a right mouse click did not work ...
    # ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)  # right mouse click
