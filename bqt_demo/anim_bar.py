"""
from bqt_demo import anim_bar
anim_bar.main()
"""
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer
import bpy


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.label1 = QtWidgets.QLabel("Changing the current frame in blender updates this slider.")
        self.label2 = QtWidgets.QLabel("Changing this slider updates the current frame in blender.")
        self.slider = QtWidgets.QSlider(Qt.Horizontal)

        with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
            self.slider.setMinimum(bpy.context.scene.frame_start)
            self.slider.setMaximum(bpy.context.scene.frame_end)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.label1)
        self.layout().addWidget(self.label2)
        self.layout().addWidget(self.slider)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_update)

        self.slider.valueChanged.connect(self.slider_changed)

    def show(self):
        super(Window, self).show()
        tick = int(1000 / 30)  # tick 1000 / frames per second
        self.timer.start(tick)

    def on_update(self):
        """set slider to current frame from blender"""
        index = bpy.context.scene.frame_current
        self.slider.setValue(index)

    def slider_changed(self, value):
        # note that if this fails blender will crash, to prevent you can use try/except
        bpy.context.scene.frame_set(value)

        # TODO add click support, currently it only works when you drag the slider


def main():
    main_window = QtWidgets.QApplication.instance().blender_widget
    w = Window(main_window)
    w.show()
    return w
