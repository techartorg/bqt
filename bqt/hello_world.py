"""
A demonstration script showing how to parent a QDialog to the Blender main window.
Yes, this could be done with QtWidgets.QMessageBox more easily.
The point is to show how to parent a window to the Blender application.

**Author:**

    Jeff Hanna, jeff.b.hanna@gmail.com, June 1, 2020
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel


class HelloWorldDialog(QDialog):
    """
    A sample 'Hello World!' QDialog.

    **Arguments:**

        None

    **Keyword Arguments:**

        None

    **Author:**

        Jeff Hanna, jeff.b.hanna@gmail.com, June 1, 2020
    """

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.resize(200, 50)
        self.setWindowTitle('Qt for Python in Blender')

        lbl_hw = QLabel('Hello World!')

        main_layout = QHBoxLayout()
        main_layout.addWidget(lbl_hw)
        self.setLayout(main_layout)


def demo():
    main_window = QApplication.instance().blender_widget
    dlg = HelloWorldDialog(main_window)
    dlg.show()


if __name__ == '__main__':
    demo()
