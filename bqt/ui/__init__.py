from pathlib import Path
from PySide2.QtGui import QImage, QPixmap
import PySide2.QtCore as QtCore


def get_question_pixmap() -> QPixmap:
    """Return the question image used in the quit dialogue"""
    icon_filepath = Path(__file__).parent / "question.svg"
    pixmap = QPixmap()
    if icon_filepath.exists():
        image = QImage(str(icon_filepath))
        if not image.isNull():
            pixmap = pixmap.fromImage(image)
            pixmap = pixmap.scaledToWidth(64, QtCore.Qt.SmoothTransformation)
    return pixmap