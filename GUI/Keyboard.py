from PyQt6 import QtWidgets, uic
import sys
from GUI.Keytop import KeyTop
from typing import Callable, Any, Iterable

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = Keyboard()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.form_widget.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
        self.show()


class Keyboard(QtWidgets.QWidget):
    def __init__(self,
                 handler: callable([str, list[str]]) = lambda x: print("Keyboard handler [" + x + "]"),
                 assets_dir: str = "../assets"):

        super(Keyboard, self).__init__()
        uic.loadUi(assets_dir + '/ui/keyboard.ui', self)

        self.assets_dir:str = assets_dir
        keyRowsMap = {self.keyboardFirstRowView: "qwertyuiop",
                      self.keyboardSecondRowView: "asdfghjkl",
                      self.keyboardThirdRowView: "zxcvbnm"}

        self.keyMap: dict[str, KeyTop] = {}

        for key in keyRowsMap:
            key.setLayout(QtWidgets.QHBoxLayout())
            for letter in keyRowsMap[key]:
                keyTop = KeyTop(letter, assets_dir=self.assets_dir)
                self.keyMap[letter] = keyTop
                key.layout().addWidget(keyTop)

        self.setKeyboardListner(handler)

    def getToggleKeys(self) -> list[str]:
        keys = []
        for key in self.keyMap:
            if self.keyMap[key].isDisabled():
                keys.append(key.upper())
        return keys

    def setKeyListner(self, key: str, handler: callable([str, list[str]]), append: bool = False) -> None:
        self.keyMap[key].setKeyListner(lambda x: handler(x, self.getToggleKeys()), append)

    def setKeyboardListner(self, handler: callable([str, list[str]]), append: bool = False) -> None:
        for key in self.keyMap:
            self.keyMap[key].setKeyListner(lambda x: handler(x, self.getToggleKeys()), append)

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