import sys

from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets, uic

from Score import Score


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = ScoreView()
        self.setStyleSheet("""background-color: black""")
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.form_widget.addScore(Score.CORRECT)
        self.form_widget.addScore(Score.CORRECT)
        self.show()


class ScoreView(QtWidgets.QWidget):
    def __init__(self, assets_dir: str = "../assets"):
        super(ScoreView, self).__init__()
        uic.loadUi(assets_dir + '/ui/scoreView.ui', self)

        self.confirmed_score = 0
        self.score_feed: list[Score] = []
        self.onHandler = lambda x, y, words: [self.addScore(Score.CORRECT) for x in  range(sum([char == x for char in words.upper()]))]

        self.offHandler = lambda x, y, words: print()
        self.scoreHandler = lambda x, y, words: print()
        self.attachHandler()
        self.updateUI()

    def updateUI(self):
        self.scoreNum.setText(str(self.getTotalScore()))

    def getTotalScore(self):
        return self.confirmed_score + sum([x.value for x in self.score_feed])

    def detachHandler(self):
        self.scoreHandler = self.offHandler

    def attachHandler(self):
        self.scoreHandler = self.onHandler

    def addScore(self, score: Score):
        self.score_feed.append(score)
        self.updateUI()

    def confirmScore(self):
        self.confirmed_score = self.getTotalScore()
        self.score_feed = []
        self.updateUI()

    def reset(self) -> None:
        self.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()