from PyQt6 import QtWidgets, uic
from PyQt6 import QtCore, QtGui
import sys

from GUI.HangmanView import HangmanView


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = Home()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        self.show()


class Home(QtWidgets.QWidget):
    def __init__(self, buttonHandler=lambda: print("Jump action"), assets_dir: str = "../assets"):
        super(Home, self).__init__()
        uic.loadUi(assets_dir + '/ui/home.ui', self)
        self.assets_dir = assets_dir

        self.hangmanView.setLayout(QtWidgets.QHBoxLayout())
        self.hangmanView.layout().addWidget(HangmanView(progress=1, assets_dir=self.assets_dir))
        self.setJumpAction(buttonHandler)

    def setJumpAction(self, handler):
        self.easyButton.clicked.connect(handler)
        self.normalButton.clicked.connect(handler)
        self.hardButton.clicked.connect(handler)

    def reset(self) -> None:
        self.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()