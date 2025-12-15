from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


def get_question_pixmap() -> QPixmap:
    """Return the question image used in the quit dialogue"""
    icon_filepath = Path(__file__).parent / "question.svg"
    pixmap = QPixmap()
    if icon_filepath.exists():
        image = QImage(str(icon_filepath))
        if not image.isNull():
            pixmap = pixmap.fromImage(image)
            pixmap = pixmap.scaledToWidth(
                64, Qt.TransformationMode.SmoothTransformation
            )
    return pixmap
