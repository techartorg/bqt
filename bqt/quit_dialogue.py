import bpy
from PySide2.QtWidgets import QMessageBox
import os


def shutdown_blender(*args):
    # # this triggers the default blender close event, showing the save dialog if needed
    # bpy.ops.wm.quit_blender({"window": bpy.context.window_manager.windows[0]}, "INVOKE_DEFAULT")
    bpy.ops.wm.quit_blender()


class WINDOW_OT_SaveFileFromQt(bpy.types.Operator):
    """Saves current Blender file and all modified images"""
    bl_idname = "wm.save_from_qt"
    bl_label = "Save_from_Qt"

    def execute(self, context):
        # TODO not sure what we are doing here, Friederman?
        if context.blend_data.is_saved:
            bpy.ops.wm.save_mainfile('EXEC_AREA', check_existing=False)
        else:
            bpy.ops.wm.save_mainfile('INVOKE_AREA', check_existing=False)
        # https://docs.blender.org/api/current/bpy.ops.html
        # EXEC_AREA - execute the operator in a certain context
        return {'FINISHED'}


class BlenderClosingDialog(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent) #, Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Save changes before closing?")
        filepath = bpy.data.filepath
        if not filepath:
            filepath = 'untitled.blend'
        filename = os.path.split(filepath)[1]
        self.setText(filename)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        self.setIcon(QMessageBox.Question)

    def execute(self):
        choice = self.exec_()
        if choice == QMessageBox.Yes:
            bpy.utils.register_class(WINDOW_OT_SaveFileFromQt)
            bpy.app.handlers.save_post.append(shutdown_blender)
            bpy.ops.wm.save_from_qt()
        if choice == QMessageBox.No:
            shutdown_blender()
        else:  # user clicked cancel
            pass
