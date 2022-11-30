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
        self.form_widget.addScore(Score.CORRECT())
        self.form_widget.addScore(Score.CORRECT())
        self.show()


class ScoreView(QtWidgets.QWidget):
    """
        Simple Button Class for the Hangman game UI.

        This can add the flexible button to the hangman UI with text, button function, custom colors (background, foreground, border)

    """
    def __init__(self, assets_dir: str = "../assets"):
        super(ScoreView, self).__init__()
        uic.loadUi(assets_dir + '/ui/scoreView.ui', self)

        self.confirmed_score = 0
        """ Confirmed score from the previous matches"""
        self.score_feed = []
        """ Life of score feed added to the ScoreView"""

        self.updateUI()

    def getFeed(self, limit: int = 5) :
        return self.score_feed if len(self.score_feed) < limit else self.score_feed[: limit]

    def updateUI(self):
        self.scoreNum.setText(str(self.getTotalScore()))

    def getTotalScore(self):
        return self.confirmed_score + sum([x.value for x in self.score_feed])

    def addScore(self, score: Score):
        self.score_feed.insert(0, score)
        self.updateUI()

    def confirmScore(self):
        self.confirmed_score = self.getTotalScore()
        self.score_feed = []
        self.updateUI()

    def reset(self) -> None:
        self.score_feed = []


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()