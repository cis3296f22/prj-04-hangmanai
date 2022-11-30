import sys

from PyQt6 import QtWidgets, uic, QtCore


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.form_widget = CharacterBox()
        self.setStyleSheet("background-color: rgb(52, 50, 48);")
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(
            lambda: self.form_widget.wrongChar() if self.form_widget.isShown() else self.form_widget.showChar()
        )
        self.timer.start(1000)
        self.form_widget.hideChar()


class CharacterBox(QtWidgets.QWidget):
    def __init__(self, text: str = "A", assets_dir: str = "../assets"):
        super(CharacterBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/characterBox_simple.ui', self)
        self.setText(text)

    def text(self) -> str:
        return self.label.text()

    def setText(self, text: str) -> None:
        self.label.setText(text.upper())

    def wrongChar(self):
        self.setDisabled(True)
        self.label.show()

    def showChar(self) -> None:
        self.setDisabled(False)
        self.label.show()

    def hideChar(self) -> None:
        self.setDisabled(True)
        self.label.hide()

    def isShown(self) -> bool:
        return self.label.isEnabled()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
