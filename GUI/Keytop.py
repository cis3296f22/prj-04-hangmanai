from PyQt6 import QtWidgets, uic
import sys

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = KeyTop(toggle=False)
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        self.show()


class KeyTop(QtWidgets.QWidget):
    def __init__(self, text="A", toggle=True):
        super(KeyTop, self).__init__()
        uic.loadUi('../assets/ui/keytop_modern.ui', self)
        self.setText(text)
        self.char = text
        self.toggle = toggle
        self.setKeyListner(lambda x: print("Default handler [" + x + "]"))
        # print(self.isEnabled())
        # self.button.setDisabled(True)
        # self.background.setDisabled(True)

    def text(self):
        return self.char

    def setText(self, text):
        self.char = text
        self.button.setText(text.upper())

    # def mousePressEvent(self, a0):
    #     print("Mouse clicked")
    #     # self.keyBackFrame.setStylesheet()

    def mouseReleaseEvent(self, a0):
        # print(self.text())
        if self.toggle:
            self.setDisabled(True)


    def isEnabled(self):
        return self.button.isEnabled()

    def setDisabled(self, boolean):
        super(KeyTop, self).setDisabled(boolean)
        # self.disabled = boolean

    def reset(self):
        self.setEnabled(True)

    def setKeyListner(self, handler, append=False):
        if not append:
            self.button.disconnect()
        self.button.clicked.connect(
            lambda: [self.mouseReleaseEvent(None), handler(self.text())]
        )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()