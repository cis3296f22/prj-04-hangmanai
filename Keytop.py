from PyQt6 import QtWidgets, uic
import sys

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = KeyTop()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        self.show()


class KeyTop(QtWidgets.QWidget):
    def __init__(self, text="A"):
        super(KeyTop, self).__init__()
        uic.loadUi('keytop_modern.ui', self)
        self.setText(text)
        self.clicked = False
        self.disabled = False
        self.setKeyListner(lambda x: print("Default handler [" + x + "]"))
        # print(self.isEnabled())
        # self.button.setDisabled(True)
        # self.background.setDisabled(True)

    def text(self):
        return self.button.text()

    def setText(self, text):
        self.button.setText(text.upper())

    # def mousePressEvent(self, a0):
    #     print("Mouse clicked")
    #     # self.keyBackFrame.setStylesheet()

    def mouseReleaseEvent(self, a0):
        # print(self.text())
        self.setDisabled(True)


    def isEnabled(self):
        return self.button.isEnabled()

    def setDisabled(self, boolean):
        super(KeyTop, self).setDisabled(boolean)
        # self.disabled = boolean

    def reset(self):
        self.clicked = False
        self.disabled = False

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