import sys

from PyQt6 import QtWidgets, uic

from Display.HangmanView import HangmanView
from WordProvider import Difficulty

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = Home()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)
        self.show()


class Home(QtWidgets.QWidget):
    """
        Home UI that is used to select the difficulty and camera used in the game.

        This is default UI that user will see when game is opened

    """

    def __init__(self, buttonHandler: callable(str) = lambda x: print(x), assets_dir: str = "../assets"):
        super(Home, self).__init__()
        uic.loadUi(assets_dir + '/ui/home_v3.ui', self)
        self.assets_dir = assets_dir
        """ Path to asset directory"""

        self.hangmanView.setLayout(QtWidgets.QHBoxLayout())
        self.hangmanView.layout().setContentsMargins(0, 0, 0, 0)
        self.hangmanView.layout().addWidget(HangmanView(progress=1, assets_dir=self.assets_dir))

        self.setDifficultyAction(buttonHandler)

    def setDifficultyAction(self, handler) -> None:
        """
            Sets the callback function to the difficulty button in Home UI

            Parameters:
            handler (callable): Callback function attached to the difficulty button

            Returns:
            None

        """
        self.easyButton.clicked.connect(lambda: handler(Difficulty.EASY))
        self.normalButton.clicked.connect(lambda: handler(Difficulty.NORMAL))
        self.hardButton.clicked.connect(lambda: handler(Difficulty.HARD))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()