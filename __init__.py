"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from bpy.types import AddonPreferences

from . import bqt

bl_info = {
    "name": "bqt",
    "description": "Plugin to help bootstrap PySide2 with an event loop within Blender",
    "author": "Tech-Artists.org",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "category": "System",
    "warning": "",
    "wiki_url": "https://github.com/techartorg/bqt",
    "tracker_url": "https://github.com/techartorg/bqt/issues"
}


class BQTAddonPreferences(AddonPreferences):
    """
    This must match the add-on name, use '__package__'
    when defining this in a submodule of a python package.
    """
    bl_idname = __package__

    def draw(self, context):
        """
        Add-on Interface elements
        Args:
            context: Blender context
        """
        layout = self.layout
        column = layout.column()

        box = column.box()
        box.row().label(text="PREFERENCES")
        box.row().label(text="<Add Content Here>")


def register():
    bpy.utils.register_class(BQTAddonPreferences)
    bqt.register()


def unregister():
    bqt.unregister()
    bpy.utils.unregister_class(BQTAddonPreferences)
