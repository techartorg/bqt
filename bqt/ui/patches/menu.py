import bpy
from bl_ui import space_topbar


class FullscreenOperator(bpy.types.Operator):
    bl_idname = "wm.window_fullscreen_qt_toggle"
    bl_label = "Toggle Window Fullscreen"
    bl_description = "Toggle the current window full-screen"

    def execute(self, context):
        from bqt import get_application
        app = get_application()
        if app.blender_widget.isFullScreen():
            app.blender_widget.showNormal()
        else:
            app.blender_widget.showFullScreen()
        return {"FINISHED"}


class TOPBAR_MT_window(bpy.types.Menu):
    """Copied from Blender 5.0.0

    scripts/startup/bl_ui/space_topbar.py
    """


    bl_label = "Window"

    def draw(self, context):
        import sys
        from _bl_ui_utils.layout import operator_context

        layout = self.layout

        layout.operator("wm.window_new")
        layout.operator("wm.window_new_main")

        layout.separator()

        # Changed from shipped menu.
        layout.operator("wm.window_fullscreen_qt_toggle", icon='FULLSCREEN_ENTER')

        layout.separator()

        layout.operator("screen.workspace_cycle", text="Next Workspace").direction = 'NEXT'
        layout.operator("screen.workspace_cycle", text="Previous Workspace").direction = 'PREV'

        layout.separator()

        layout.prop(context.screen, "show_statusbar")

        layout.separator()

        layout.operator("screen.screenshot")

        # Showing the status in the area doesn't work well in this case.
        # - From the top-bar, the text replaces the file-menu (not so bad but strange).
        # - From menu-search it replaces the area that the user may want to screen-shot.
        # Setting the context to screen causes the status to show in the global status-bar.
        with operator_context(layout, 'INVOKE_SCREEN'):
            layout.operator("screen.screenshot_area")

        if sys.platform[:3] == "win":
            layout.separator()
            layout.operator("wm.console_toggle", icon='CONSOLE')

        if context.scene.render.use_multiview:
            layout.separator()
            layout.operator("wm.set_stereo_3d")



def register():
    bpy.utils.unregister_class(space_topbar.TOPBAR_MT_window)
    bpy.utils.register_class(FullscreenOperator)
    bpy.utils.register_class(TOPBAR_MT_window)


def unregister():
    bpy.utils.register_class(space_topbar.TOPBAR_MT_window)
    bpy.utils.unregister_class(FullscreenOperator)
    bpy.utils.unregister_class(TOPBAR_MT_window)
