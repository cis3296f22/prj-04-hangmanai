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
        uic.loadUi('keytop.ui', self)
        self.text(text)

    def text(self, text):
        self.label.setText(text.upper())

    def mousePressEvent(self, a0):
        print("Mouse clicked")
        # self.keyBackFrame.setStylesheet()


    def mouseReleaseEvent(self, a0):
        print()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()