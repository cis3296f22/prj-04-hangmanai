import sys

from PyQt6 import QtWidgets, uic, QtGui

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
            print(e.text().upper())

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        if not e.isAutoRepeat():
            self.form_widget.trigger(e.text())


class Keyboard(QtWidgets.QWidget):

    """
        Virtual keyboard in Main Game UI and is used to choose alphabet and show the availability of the characters

    """
    def __init__(self,
                 handler=lambda x, y: print("[" + x + "] -> " + str(y)),
                 assets_dir: str = "../assets"):

        super(Keyboard, self).__init__()
        uic.loadUi(assets_dir + '/ui/keyboard.ui', self)

        self.assets_dir: str = assets_dir
        """ Path to asset directory"""
        self.keyMap: dict[str, KeyTop] = {}
        """ Map of string alphabet to the corresponding Keptop object"""

        keyRowsMap = {self.keyboardFirstRowView: "qwertyuiop".upper(),
                      self.keyboardSecondRowView: "asdfghjkl".upper(),
                      self.keyboardThirdRowView: "zxcvbnm".upper()}

        for key in keyRowsMap:
            key.setLayout(QtWidgets.QHBoxLayout())
            for letter in keyRowsMap[key]:
                keyTop = KeyTop(letter, assets_dir=self.assets_dir)
                self.keyMap[letter] = keyTop
                key.layout().addWidget(keyTop)

        self.setKeyboardListner(handler)

    def getToggleKeys(self):
        """
            Returns the list of the toggled keys in the keyboard

            Returns:
            list[str]: List of the selected or toggled key in char

        """
        keys = []
        for key in self.keyMap:
            if self.keyMap[key].isDisabled():
                keys.append(key.upper())
        return keys

    def setKeyboardListner(self, handler, append: bool = False) -> None:
        """
            Sets the callback function to each keyboard keys

            Parameters:
            handler (callable): Callback function that will be executed when the specified key is clicked
            append (bool): Handler will be appended to the existing handler

            Returns:
            None

        """
        for key in self.keyMap:
            self.keyMap[key].setKeyListner(lambda x: handler(x, self.getToggleKeys()), append)

    def reset(self) -> None:
        """
            Resets the all toggled keys

            Returns:
            None

        """
        for key in self.keyMap:
            self.keyMap[key].reset()

    def trigger(self, key) -> None:
        """
            Trigger the click of the specified key

            Parameters:
            key (str): Key in a keyboard that you want to trigger

            Returns:
            None

        """
        key = key.upper()
        if key not in self.keyMap.keys():
            return
        self.keyMap[key].trigger()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
