"""
A demonstration script showing how to parent a QDialog to the Blender main window.
Yes, this could be done with QtWidgets.QMessageBox more easily.
The point is to show how to parent a window to the Blender application.

from bqt_demo import hello_world
hello_world.demo()
"""

import PySide6

Qt = PySide6.QtCore.Qt
QApplication = PySide6.QtWidgets.QApplication
QDialog = PySide6.QtWidgets.QDialog
QHBoxLayout = PySide6.QtWidgets.QHBoxLayout
QLabel = PySide6.QtWidgets.QLabel


class HelloWorldDialog(QDialog):
    """
    A sample 'Hello World!' QDialog.
    """

    def __init__(self, parent):
        super().__init__(
            parent,
            Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint,
        )

        self.resize(200, 50)
        self.setWindowTitle("Qt for Python in Blender")

        lbl_hw = QLabel("Hello World!")

        main_layout = QHBoxLayout()
        main_layout.addWidget(lbl_hw)
        self.setLayout(main_layout)


def demo():
    main_window = QApplication.instance().blender_widget
    dlg = HelloWorldDialog(main_window)
    dlg.show()


if __name__ == "__main__":
    demo()
