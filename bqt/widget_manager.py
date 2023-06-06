"""
widget manager to register your widgets with bqt

- parent widget to blender window (blender_widget)
- keep widget in front of Blender window only, even when bqt is not wrapped in qt
"""
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
import logging


__widgets = []


class WidgetData():
    def __init__(self, widget, visible):
        self.widget = widget
        self.visible = visible


def add(widget):
    """parent widget to blender window"""
    if not widget:
        logging.warning("bqt: widget is None, skipping widget registration")
        return

    app = QApplication.instance()

    # parent to blender window
    widget.setParent(app.blender_widget)

    # save widget so we can manage the focus and visibility
    data = WidgetData(widget, widget.isVisible())  # todo can we init vis state to false?
    __widgets.append(data)


def iter_widget_data():
    """iterate over all registered widgets, remove widgets that have been removed"""
    cleanup = []
    for widget_data in __widgets:
        if not widget_data.widget:
            cleanup.append(widget_data)
            continue
        yield widget_data
    for widget_data in cleanup:
        __widgets.remove(widget_data)


def _blender_window_change(focussed_on_a_blender_window: bool):
    for widget_data in iter_widget_data():
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