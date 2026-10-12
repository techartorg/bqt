"""Translate Blender's live UI theme into a QPalette

Approach ported & trimmed from https://github.com/minimalefforttech/blender_qt/tree/main/blender_qt/theme
"""

from __future__ import annotations

from collections.abc import Sequence

import bpy
from PySide6.QtGui import QColor, QPalette


def _to_qcolor(value: Sequence[float], background: QColor | None = None) -> QColor:
    """Blender RGBA float tuple to an opaque QColor, composited over background"""
    try:
        red, green, blue = float(value[0]), float(value[1]), float(value[2])
    except (IndexError, TypeError, ValueError):
        red, green, blue = 0.0, 0.0, 0.0
    try:
        alpha = float(value[3])
    except (IndexError, TypeError, ValueError):
        alpha = 1.0

    if background is not None and alpha < 1.0:
        alpha = max(0.0, min(1.0, alpha))
        inverse = 1.0 - alpha
        red = red * alpha + background.redF() * inverse
        green = green * alpha + background.greenF() * inverse
        blue = blue * alpha + background.blueF() * inverse

    return QColor(int(red * 255), int(green * 255), int(blue * 255))


def _mix(color_a: QColor, color_b: QColor, factor: float) -> QColor:
    """Linearly interpolate between two colours"""
    factor = max(0.0, min(1.0, factor))
    inverse = 1.0 - factor
    return QColor(
        int(color_a.red() * inverse + color_b.red() * factor),
        int(color_a.green() * inverse + color_b.green() * factor),
        int(color_a.blue() * inverse + color_b.blue() * factor),
    )


def _widget_color(
    widgets: Sequence[bpy.types.ThemeWidgetColors | None],
    attribute: str,
    fallback: Sequence[float],
    background: QColor | None = None,
) -> QColor:
    """Return the first attribute found across a priority list of widgets"""
    for widget in widgets:
        if widget is not None and hasattr(widget, attribute):
            return _to_qcolor(getattr(widget, attribute), background=background)
    return _to_qcolor(fallback, background=background)


def build_blender_palette() -> QPalette:
    """Read the active Blender theme and produce a QPalette"""
    ui = bpy.context.preferences.themes[0].user_interface

    regular = getattr(ui, "wcol_regular", None)
    text = getattr(ui, "wcol_text", regular)
    num = getattr(ui, "wcol_num", text)
    list_item = getattr(ui, "wcol_list_item", text)
    menu = getattr(ui, "wcol_menu", regular)
    menu_back = getattr(ui, "wcol_menu_back", menu)
    tooltip = getattr(ui, "wcol_tooltip", regular)
    box = getattr(ui, "wcol_box", regular)

    panel_back = _to_qcolor(
        getattr(ui, "panel_back", getattr(box, "inner", (0.18, 0.18, 0.18)))
    )

    window = panel_back
    window_text = _widget_color([regular, text], "text", (0.94, 0.94, 0.94))
    base = _widget_color(
        [text, num, regular, menu], "inner", (0.14, 0.14, 0.14), panel_back
    )
    text_color = _widget_color([text, num, regular], "text", (0.94, 0.94, 0.94))
    button = _widget_color(
        [regular, menu_back, text], "inner", (0.22, 0.22, 0.22), panel_back
    )
    button_text = _widget_color([regular, menu_back, text], "text", (0.94, 0.94, 0.94))
    tooltip_base = _widget_color(
        [tooltip, text, num], "inner", (0.14, 0.14, 0.14), panel_back
    )
    tooltip_text = _widget_color([tooltip, regular], "text", (0.94, 0.94, 0.94))
    highlight = _widget_color(
        [list_item, regular, num], "inner_sel", (0.28, 0.45, 0.7), panel_back
    )
    highlighted_text = _widget_color([num, text, regular], "text_sel", (1.0, 1.0, 1.0))
    border = _widget_color(
        [box, menu_back, regular], "outline", (0.3, 0.3, 0.3), panel_back
    )

    # wcol_list_item.inner is a white tint Blender modulates internally, so derive
    # the alternate row from the base instead.
    alternate_base = _mix(base, window, 0.32)

    light = _mix(button, QColor("#ffffff"), 0.18)
    midlight = _mix(button, light, 0.45)
    mid = _mix(button, border, 0.45)
    dark = _mix(button, window, 0.4)
    shadow = _mix(dark, QColor("#000000"), 0.5)
    muted_text = _mix(text_color, window, 0.42)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, window)
    palette.setColor(QPalette.ColorRole.WindowText, window_text)
    palette.setColor(QPalette.ColorRole.Base, base)
    palette.setColor(QPalette.ColorRole.AlternateBase, alternate_base)
    palette.setColor(QPalette.ColorRole.Text, text_color)
    palette.setColor(QPalette.ColorRole.Button, button)
    palette.setColor(QPalette.ColorRole.ButtonText, button_text)
    palette.setColor(QPalette.ColorRole.ToolTipBase, tooltip_base)
    palette.setColor(QPalette.ColorRole.ToolTipText, tooltip_text)
    palette.setColor(QPalette.ColorRole.Highlight, highlight)
    palette.setColor(QPalette.ColorRole.HighlightedText, highlighted_text)
    palette.setColor(QPalette.ColorRole.Light, light)
    palette.setColor(QPalette.ColorRole.Midlight, midlight)
    palette.setColor(QPalette.ColorRole.Mid, mid)
    palette.setColor(QPalette.ColorRole.Dark, dark)
    palette.setColor(QPalette.ColorRole.Shadow, shadow)
    palette.setColor(QPalette.ColorRole.PlaceholderText, muted_text)
    palette.setColor(QPalette.ColorRole.Link, highlight)

    # Disabled colour group — keep disabled widgets readable.
    disabled_text = _mix(text_color, window, 0.6)
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled,
        QPalette.ColorRole.ButtonText,
        _mix(button_text, button, 0.55),
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, _mix(base, window, 0.3)
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled,
        QPalette.ColorRole.Button,
        _mix(button, window, 0.35),
    )

    return palette
