from PyQt6 import QtWidgets, uic, QtCore
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QPushButton


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = KeyTop(toggle=True)
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.form_widget.trigger)
        self.timer.start(1000)


class KeyTop(QtWidgets.QWidget):
    def __init__(self,
                 text: str = "A",
                 toggle: bool = True,
                 handler: callable(str) = lambda x: print("Default handler [" + x + "]"),
                 assets_dir: str = "../assets"):

        super(KeyTop, self).__init__()
        uic.loadUi(assets_dir + '/ui/keytop_modern_v2.ui', self)
        self.setText(text)
        self.char: str = text
        self.toggle: bool = toggle
        self.setKeyListner(handler)

    def text(self) -> str:
        return self.char

    def setText(self, text: str) -> None:
        self.char = text
        self.button.setText(text.upper())

    def mouseReleaseEvent(self, a0):
        # print(self.text())
        if self.toggle:
            self.setDisabled(True)

    def isDisabled(self) -> bool:
        return not self.button.isEnabled()

    def reset(self):
        self.setEnabled(True)

    def setKeyListner(self, handler: callable(str), append: bool = False) -> None:
        if not append:
            self.button.disconnect()
        self.button.clicked.connect(
            lambda: [self.mouseReleaseEvent(None), handler(self.text().upper())]
        )

    def trigger(self):
        if self.isDisabled():
            return
        # self.mouseReleaseEvent(None)
        self.button.click()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()