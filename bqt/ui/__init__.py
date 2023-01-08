from pathlib import Path
from PySide6.QtGui import QImage, QPixmap
import PySide6.QtCore as QtCore


def get_question_pixmap():
    icon_filepath = Path(__file__).parents[1] / "images" / "question.svg"
    pixmap = QPixmap()
    if icon_filepath.exists():
        image = QImage(str(icon_filepath))
        if not image.isNull():
            pixmap = pixmap.fromImage(image)
            pixmap = pixmap.scaledToWidth(64, QtCore.Qt.SmoothTransformation)
    return pixmap


__all__ = ["get_question_pixmap"]
