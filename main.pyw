from PyQt6 import QtWidgets, uic
import sys

from keytop import KeyTop


class MyMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.form_widget = Ui()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(KeyTop())
        layout.addWidget(KeyTop())
        layout.addWidget(KeyTop())
        self.form_widget.keyboardFirstRowView.setLayout(layout)
        self.form_widget.keyboardFirstRowView.setStyleSheet("background-color: rgb(255,255,255);")
        self.show()


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyMainWindow()
    app.exec()