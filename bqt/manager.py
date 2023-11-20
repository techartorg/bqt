"""
widget manager to register your widgets with bqt

- parent widget to blender window (blender_widget)
- keep widget in front of Blender window only, even when bqt is not wrapped in qt
"""
from bqt.qt_core import QApplication, QDockWidget, QtCore
import logging
import os
logger = logging.getLogger("bqt")



__widgets = []
__excluded_widgets = []


class WidgetData():
    def __init__(self, widget, visible):
        self.widget = widget
        self.visible = visible


def make_widget_dockable(widget):
    """wrap widget in QDockWidget if not already"""
    if not isinstance(widget, QDockWidget):
        logger.debug("wrapping widget in QDockWidget")

        dock_widget = QDockWidget()
        dock_widget.setWindowFlags(widget.windowFlags())
        dock_widget.setWidget(widget)
        widget.setParent(dock_widget)

        # title
        title = widget.windowTitle() or widget.objectName() or "widget"
        dock_widget.setWindowTitle(title)

        # object name
        obj_name = widget.objectName()
        if obj_name:
            dock_widget.setObjectName(f"dockable_{obj_name}")

        # bit hacky todo cleanup
        widget.show()
        dock_widget.show()

        return dock_widget
    return widget


def register(widget, exclude=None, parent=True, manage=True, unique=True):
    """
    parent widget to blender window
    Args:
        widget: child widget to parent
        parent: if True, parent the widget to the blender window
        exclude: widgets to exclude from being parented to the blender window
        manage: if True, manage the visibility of the widget
        unique: if True, prevent registering a new widget with the same objectName
    """
    exclude = exclude or []
    logger.debug(f"registering widget with bqt '{widget}'")

    if not widget:
        logger.warning("widget is None, skipping registration")
        return

    parent_widget = QApplication.instance().blender_widget
    if widget == parent_widget:
        logger.warning("widget equals parent, skipping registration")
        return

    if os.getenv("BQT_DOCKABLE_WRAP", "1") == "1":
        widget = make_widget_dockable(widget)

    # prevent registering a new widget with the same objectName
    if unique and os.getenv("BQT_UNIQUE_OBJECTNAME", "1") == "1":
        obj_name = widget.objectName()
        old_widget = None  # already registered widget with the same objectName
        if obj_name:
            for data in iter_widget_data():
                if data.widget.objectName() == obj_name:
                    old_widget = data.widget
                    break
        if old_widget:
            logger.warning("widget is already registered, skipping widget registration")
            # show old widget, delete new widget
            old_widget.show()
            old_widget.activateWindow()
            widget.deleteLater()  # delete duplicate widget, todo dangerous?
            __excluded_widgets.append(widget)
            return

    if widget in exclude:
        logger.warning("widget is in exclude list, skipping widget registration")
        return

    # parent to blender window
    if parent:
        logger.debug("parenting widget to blender window")
        vis = widget.isVisible()
        widget.setParent(parent_widget, QtCore.Qt.Window)  # default set flag to window
        widget.setVisible(vis)  # parenting hides the widget, restore visibility

    # save widget so we can manage the focus and visibility
    if manage:
        data = WidgetData(widget, widget.isVisible())  # todo can we init vis state to false?
        __widgets.append(data)

        # ensure widget stays in foreground if blender is not wrapped in qt
        if os.getenv("BQT_DISABLE_WRAP", "0") == "1" and os.getenv("BQT_MANAGE_FOREGROUND", "1") == "1":
            logger.debug("setting widget WindowStaysOnTopHint")
            vis = widget.isVisible()
            widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            widget.setVisible(vis)


def iter_widget_data():
    """iterate over all registered widgets, remove widgets that have been removed"""
    cleanup = []
    for widget_data in __widgets:
        if not widget_data.widget:
            cleanup.append(widget_data)
            continue

        try:
            v = widget_data.widget.isVisible()
        except RuntimeError:
            cleanup.append(widget_data)
            continue

        yield widget_data
    for widget_data in cleanup:
        __widgets.remove(widget_data)


def _blender_window_change(hwnd: int):
    """
    hide widgets when blender is not focussed,
    keep widgets in front of the Blender window when Blender is focussed
    run when changing between a blender & non-blender window
    """
    focussed_on_a_blender_window = hwnd != 0  # 0 for windows not created by blender

    for widget_data in iter_widget_data():
        widget = widget_data.widget

        if focussed_on_a_blender_window:

            # add top flag, ensure the widget stays in front of the blender window
            # widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # todo move this to register?

            # restore visibility state of the widget
            if widget_data.visible:
                widget.show()

        else:  # non-blender window
            # save visibility state of the widget
            widget_data.visible = widget.isVisible()

            # remove top flag, allow the widget to be hidden behind the blender window
            # self.blender_widget2.setWindowFlags(self.blender_widget2.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            widget.hide()  # todo since we hide do we need to remove flag?

    # todo right now widgets stay in front of other blender windows,
    #  e.g. the preferences window, ideally we handle this


def _orphan_toplevel_widgets():
    return [widget for widget in QApplication.instance().topLevelWidgets() if
            not widget.parent()
            and widget not in __widgets
            and widget not in __excluded_widgets]


def parent_orphan_widgets(exclude=None):
    """Find and parent orphan widgets to the blender widget"""
    # this runs every frame, don't print or log in this method
    exclude = exclude or []
    __excluded_widgets.extend(exclude)
    for widget in _orphan_toplevel_widgets():
        if widget.windowType() in (QtCore.Qt.WindowType.ToolTip, ):
            __excluded_widgets.append(widget)
            continue
        elif not widget.windowType() in (QtCore.Qt.Window, QtCore.Qt.Dialog, ):
            logger.warning(f"skipping widget: '{widget}' not window type but {widget.windowType()}")
            __excluded_widgets.append(widget)
            continue
        # todo test with various widgets, we likely exclude some valid widgets
        #  this should fail with a combobox (dropdown) and menu

        register(widget, exclude=exclude)

