from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt


widgets = []
# todo manage if widget is None, or removed


class WidgetData():
    def __init__(self, widget, visible):
        self.widget = widget
        self.visible = visible


def add(widget):
    """parent widget to blender window"""
    print("adding widget to blender window", widget)

    app = QApplication.instance()

    # parent to blender window
    widget.setParent(app.blender_widget)

    # save widget so we can manage the focus and visibility
    data = WidgetData(widget, widget.isVisible())  # todo can we init vis state to false?
    widgets.append(data)


def _blender_window_change(focussed_on_a_blender_window: bool):
    for widget_data in widgets:
        widget = widget_data.widget

        if focussed_on_a_blender_window:

            # add top flag, ensure the widget stays in front of the blender window
            widget.setWindowFlags(widget.windowFlags() | Qt.WindowStaysOnTopHint)

            # restore visibility state of the widget
            if widget_data.visible:
                widget.show()

        else:  # non-blender window
            # save visibility state of the widget
            widget_data.visible = widget.isVisible()

            # remove top flag, allow the widget to be hidden behind the blender window
            # self.blender_widget2.setWindowFlags(self.blender_widget2.windowFlags() & ~Qt.WindowStaysOnTopHint)
            widget.hide()  # todo since we hide do we need to remove flag?