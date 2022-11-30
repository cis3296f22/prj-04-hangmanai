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
        ScoreView will keep the current socre and show it to the user.

        This will keep the list of score in a match together with the sum of the score earned before the current game.

    """
    def __init__(self, assets_dir: str = "../assets"):
        super(ScoreView, self).__init__()
        uic.loadUi(assets_dir + '/ui/scoreView.ui', self)

        self.confirmed_score = 0
        """ Confirmed score from the previous matches"""
        self.score_feed = []
        """ Life of score feed added to the ScoreView"""

        self.updateUI()

    def getFeed(self, limit: int = 5):
        """
            Returns the list of score feed

            Returns:
            The list of score feed

        """
        return self.score_feed if len(self.score_feed) < limit else self.score_feed[: limit]

    def updateUI(self) -> None:
        """
            Update the score text

            Returns:
            None

        """
        self.scoreNum.setText(str(self.getTotalScore()))

    def getTotalScore(self) -> int:
        """
            Get the total score

            Parameters:
            text (str): New text in character box

            Returns:
            int: sum of the score from the match and previous matches

        """
        return self.confirmed_score + sum([x.value for x in self.score_feed])

    def addScore(self, score: Score) -> None:
        """
            Add score to the score feed list

            Parameters:
            score (Score): Score to be added to the list

            Returns:
            None

        """
        self.score_feed.insert(0, score)
        self.updateUI()

    def confirmScore(self) -> None:
        """
            Override the confirmed_score with the sum of the current total score and empty the list of score feed

            Returns:
            None

        """
        self.confirmed_score = self.getTotalScore()
        self.score_feed = []
        self.updateUI()

    def reset(self) -> None:
        """
            Empties the list of score feed

            Returns:
            None

        """
        self.score_feed = []


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()