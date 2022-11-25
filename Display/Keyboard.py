import sys
import typing

from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtCore import QThread, QObject, QEvent

from Display.Keytop import KeyTop


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = Keyboard()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if not e.isAutoRepeat():
            print(e.text().upper() )

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        if not e.isAutoRepeat():
            self.form_widget.trigger(e.text())

class Keyboard(QtWidgets.QWidget):
    def __init__(self,
                 handler = lambda x, y: print("[" + x + "] -> " + str(y)),
                 assets_dir: str = "../assets"):

        super(Keyboard, self).__init__()
        uic.loadUi(assets_dir + '/ui/keyboard.ui', self)

        self.assets_dir:str = assets_dir
        keyRowsMap = {self.keyboardFirstRowView: "qwertyuiop".upper(),
                      self.keyboardSecondRowView: "asdfghjkl".upper(),
                      self.keyboardThirdRowView: "zxcvbnm".upper()}

        self.keyMap: dict[str, KeyTop] = {}

        for key in keyRowsMap:
            key.setLayout(QtWidgets.QHBoxLayout())
            for letter in keyRowsMap[key]:
                keyTop = KeyTop(letter, assets_dir=self.assets_dir)
                self.keyMap[letter] = keyTop
                key.layout().addWidget(keyTop)

        self.setKeyboardListner(handler)

    def getToggleKeys(self) :
        keys = []
        for key in self.keyMap:
            if self.keyMap[key].isDisabled():
                keys.append(key.upper())
        return keys

    def setKeyboardListner(self, handler, append: bool = False) -> None:
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

    def trigger(self, key):
        key = key.upper()
        if key not in self.keyMap.keys():
            return
        self.keyMap[key].trigger()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()