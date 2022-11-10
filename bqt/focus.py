import atexit
import os
import sys
import ctypes
import bpy
import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QApplication
from .blender_applications import BlenderApplication


# bpy.ops.bqt.return_focus
class QFocusOperator(bpy.types.Operator):
    bl_idname = "bqt.return_focus"
    bl_label = "Fix bug related to bqt focus"
    bl_description = "Fix bug related to bqt focus"
    bl_options = {'INTERNAL'}

    def __init__(self):
        super().__init__()

    def __del__(self):
        """called when the operator finishes"""
        pass

    def invoke(self, context, event):
        """
        every time blender opens a new file, the context resets, losing the focus-hook.
        Re-instantiate the hook that returns focus to blender on alt tab bug

        ensure this is not called twice! or blender might crash on load new file
        """
        # modal
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

        # # non modal, run once and exit
        # self._detect_keyboard(event)
        # return {"FINISHED"}

    def modal(self, context, event):
        """
        pass all events (e.g. keypress, mouse-move, ...) to detect_keyboard
        """
        self._detect_keyboard(event)
        return {"PASS_THROUGH"}

    def _detect_keyboard(self, event):
        """
        detect when blender receives focus, and force a release of 'stuck' keys
        """

        self._qapp = QApplication.instance()
        if not self._qapp:
            print("QApplication not yet instantiated, focus hook can't be set")
            # wait until bqt has started the QApplication
            return

        if self._qapp.just_focused:
            self._qapp.just_focused = False
            print("just focused")

            # key codes from https://itecnote.com/tecnote/python-simulate-keydown/
            keycodes = [
                ('_ALT', 0x12),
                ('_CTRL', 0x11),
                ('_SHIFT', 0x10),
                ('VK_LWIN', 0x5B),
                ('VK_RWIN', 0x5C),
                ('OSKEY', 0x5B),  # dupe oskey, blender names it this
            ]

            print("event.type", event.type, type(event.type))
            for name, code in keycodes:

                # if the first key pressed is one of the following,
                # don't simulate a key release, since it causes this bug:
                # the first keypress on re-focus blender will be ignored, e.g. ctrl + v will just be v
                if name in event.type:
                    print("skipping:", name)
                    continue

                # safely release all other keys that might be stuck down
                ctypes.windll.user32.keybd_event(code, 0, 2, 0)  # release key
                print("released key", name, code)
