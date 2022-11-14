import sys

from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets, uic


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = ScoreView()
        self.setStyleSheet("""background-color: black""")
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.form_widget.setScore(100)
        self.form_widget.addScore(100)
        self.show()


class ScoreView(QtWidgets.QWidget):
    def __init__(self, score: int = 0, assets_dir: str = "../assets"):
        super(ScoreView, self).__init__()
        uic.loadUi(assets_dir + '/ui/scoreView.ui', self)

        self.score = score
        self.setScore(self.score)

    def addScore(self, score):
        self.setScore(self.score + score)

    def setScore(self, score: int):
        self.score = score
        self.scoreNum.setText(str(self.score))

    def reset(self) -> None:
        self.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()