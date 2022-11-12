from PyQt6 import QtWidgets, uic
import sys, os
from GUI.Keytop import KeyTop


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = Keyboard()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        self.show()


class Keyboard(QtWidgets.QWidget):
    def __init__(self, handler=lambda x: print("Keyboard handler [" + x + "]"), assets_dir: str = "../assets"):
        super(Keyboard, self).__init__()
        uic.loadUi(assets_dir + '/ui/keyboard.ui', self)

        self.assets_dir:str = assets_dir
        keyRowsMap = {self.keyboardFirstRowView: "qwertyuiop",
                      self.keyboardSecondRowView: "asdfghjkl",
                      self.keyboardThirdRowView: "zxcvbnm"}

        self.keyMap: dict[str, QtWidgets.QWidget] = {}

        for key in keyRowsMap:
            key.setLayout(QtWidgets.QHBoxLayout())
            for letter in keyRowsMap[key]:
                keyTop = KeyTop(letter, assets_dir=self.assets_dir)
                self.keyMap[letter] = keyTop
                key.layout().addWidget(keyTop)

        self.setKeyboardListner(handler)

    def setKeyListner(self, key: str, handler, append: bool = False) -> None:
        self.keyMap[key].setKeyListner(handler, append)

    def setKeyboardListner(self, handler, append: bool = False) -> None:
        for key in self.keyMap:
            self.keyMap[key].setKeyListner(handler, append)

    def reset(self) -> None:
        for key in self.keyMap:
            self.keyMap[key].reset()

    def disableAll(self) -> None:
        for key in self.keyMap:
            self.keyMap[key].setDisabled(True)

    def enableAll(self) -> None:
        for key in self.keyMap:
            self.keyMap[key].setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()