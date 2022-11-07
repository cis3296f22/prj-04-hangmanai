from PyQt6 import QtWidgets, uic
import sys


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.form_widget = CharacterBox()
        self.setStyleSheet("background-color: rgb(52, 50, 48);")
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class CharacterBox(QtWidgets.QWidget):
    def __init__(self, text="A", assets_dir="../assets"):
        super(CharacterBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/characterBox.ui', self)
        self.setText(text)

    def text(self):
        return self.label.text()

    def setText(self, text):
        self.label.setText(text.upper())

    # def mousePressEvent(self, a0):
    #     print("Mouse clicked")
    #     # self.keyBackFrame.setStylesheet()

    def reset(self):
        self.clicked = False
        self.disabled = False

    def blank(self):
        self.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
