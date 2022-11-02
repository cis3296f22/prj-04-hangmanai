from PyQt6 import QtWidgets, uic
import sys
from Keytop import KeyTop

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
    def __init__(self, handler=lambda x: print("Keyboard handler [" + x + "]")):
        super(Keyboard, self).__init__()
        uic.loadUi('../assets/ui/keyboard.ui', self)
        # self.text(text)

        keyRowsMap = {self.keyboardFirstRowView: "qwertyuiop",
                      self.keyboardSecondRowView: "asdfghjkl",
                      self.keyboardThirdRowView: "zxcvbnm"}

        self.keyMap = {}

        # self.form_widget.keyboardFirstRowView.layout().addWidget(KeyTop())

        for key in keyRowsMap:
            key.setLayout(QtWidgets.QHBoxLayout())
            for letter in keyRowsMap[key]:
                keyTop = KeyTop(letter)
                self.keyMap[letter] = keyTop
                key.layout().addWidget(keyTop)

        self.setKeyboardListner(handler)

    def setKeyListner(self, key, handler, append=False):
        self.keyMap[key].setKeyListner(handler, append)

    def setKeyboardListner(self, handler, append=False):
        for key in self.keyMap:
            self.keyMap[key].setKeyListner(handler, append)

    def reset(self):
        for key in self.keyMap:
            self.keyMap[key].reset()

    def disableAll(self):
        for key in self.keyMap:
            self.keyMap[key].setDisabled(True)

    def enableAll(self):
        for key in self.keyMap:
            self.keyMap[key].setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()