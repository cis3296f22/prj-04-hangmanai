import sys

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6 import uic
from PyQt6.QtCore import (Qt)

from Display.CameraSwitchView import CameraSwitchView
from Display.CameraThread import CameraThread
from Display.HangmanView import HangmanView
from Display.Home import Home
from Display.Keyboard import Keyboard
from Display.LifeBox import LifeBox
from Display.ScoreView import ScoreView
from Display.WordBox import WordBox

from Score import Score
from WordProvider import Difficulty

WINDOW_SIZE = 0


class MainFrame(QtWidgets.QMainWindow):
    """
        Main Frame of the main hangman game.

    """

    def __init__(self,
                 parent=None,
                 keyboard_handler=lambda x, y: print("[" + x + "] -> " + str(y)),
                 difficulty_handler: callable(str) = lambda x: print(x),
                 assets_dir: str = "../assets"):

        super(MainFrame, self).__init__(parent)
        self.assets_dir: str = assets_dir
        """ Path to asset directory"""

        self.ui: Ui = Ui(assets_dir=self.assets_dir)
        """ Hangman UI. Main game UI"""
        self.home: Home = Home(buttonHandler=self.transitMainGame, assets_dir=assets_dir)
        """ Home UI"""
        self.worker = CameraThread(self.ui.cameraView, recognition_callback=self.ui.keyboard.trigger)
        """ Worker thread for smooth camera feed"""

        self.ui.hangmanDisplay.setHomeHandler(self.transitHome)
        self.setCentralWidget(self.home)
        self.keyboard_handler: callable = keyboard_handler
        self.ui.keyboard.setKeyboardListner(keyboard_handler)
        self.difficultyHandler: callable(str) = difficulty_handler

        self.home.cameraSwitchView.setLayout(QtWidgets.QHBoxLayout())
        self.home.cameraSwitchView.layout().setContentsMargins(0, 0, 0, 0)
        self.home.cameraSwitchView.layout().addWidget(CameraSwitchView(self.worker))

        self.worker.start()

        self.show()
        self.windowInit()

        # self.ui.

    def windowInit(self):
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        central_widget = self.centralWidget()
        if hasattr(central_widget, "minimizeButton"):
            central_widget.minimizeButton.clicked.connect(lambda: self.showMinimized())
        # Close window
        if hasattr(central_widget, "closeButton"):
            central_widget.closeButton.clicked.connect(lambda: self.close())
        # Restore/Maximize window
        if hasattr(central_widget, "restoreButton"):
            central_widget.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())

        def moveWindow(event):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        if hasattr(central_widget, "title_bar"):
            # Remove window tlttle bar
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

            # Set main background to transparent
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            if hasattr(central_widget, "title_bar"):
                central_widget.title_bar.mouseMoveEvent = moveWindow

        # Show window
        self.show()

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        if not e.isAutoRepeat():
            self.ui.keyboard.trigger(e.text())

    def setDifficultyHandler(self, handler: callable(str)) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        self.difficultyHandler = handler

    def transitMainGame(self, args=None) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        self.difficultyHandler(args)
        self.home = self.takeCentralWidget()
        self.setCentralWidget(self.ui)
        self.windowInit()

    def transitHome(self, args=None) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        self.ui = self.takeCentralWidget()
        self.setCentralWidget(self.home)
        self.windowInit()

    def mousePressEvent(self, event) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        self.dragPos = event.globalPosition()

    # Restore or maximize your window
    def restore_or_maximize_window(self) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """

        # Global windows state
        global WINDOW_SIZE  # The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        if win_status == 0:
            # If the window is not maximized
            WINDOW_SIZE = 1  # Update value to show that the window has been maxmized
            self.showMaximized()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))  # Show maximized icon
        else:
            # If the window is on its default size
            WINDOW_SIZE = 0  # Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()
            # Update button icon
            # self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))  # Show minized icon

    def setKeyboardListner(self, handler, append=False) -> None:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        self.ui.keyboard.setKeyboardListner(handler, append)

    def reset(self) -> None:
        """
            Resets the main frame

            Returns:
            None

        """
        self.ui.reset()

    def hideCharAt(self, index) -> None:
        """
            Hide character at an index

            Parameters:
            index (int): Index of character in a word that you want to hide

            Returns:
            None

        """
        self.ui.wordBox.hideCharAt(index)

    def showCharAt(self, index) -> None:
        """
            Show character at an index

            Parameters:
            index (int): Index of character in a word that you want to show

            Returns:
            None

        """
        self.ui.wordBox.showCharAt(index)

    def wrongChars(self) -> None:
        """
            Show the hidden characters as wrong guessed chars

            Returns:
            None

        """
        self.ui.wordBox.wrongChars()

    def setWord(self, word, hide=False) -> None:
        """
            Setter for the word in the word box

            Parameters:
            text (str): New word in word box

            Returns:
            None

        """
        self.ui.wordBox.setWord(word, hide)

    def setMaxAttempts(self, max_attempts) -> None:
        """
            Setter for the max_attempts

            Parameters:
            max_attempts (str): New max_attempts

            Returns:
            None

        """
        self.ui.lifeBox.setMaxAttempts(max_attempts)
        self.ui.hangmanDisplay.setMaxAttempts(max_attempts)

    def setLife(self, number) -> None:
        """
            Sets the life in the LifeBox

            Parameters:
            number (int): New life in int

            Returns:
            None

        """
        life = self.ui.lifeBox.getLife()
        self.ui.lifeBox.setLife(number)
        if life > number:
            self.ui.hangmanDisplay.takeDamage()

    def setReplayHandler(self, handler, append: bool = True):
        """
            Update replay button handler

            Parameters:
            handler (callable): New handler
            append (bool): True if appending the new handler to the existing handler

            Returns:
            None

        """
        self.ui.hangmanDisplay.setReplayHandler(handler, append)

    def setHomeHandler(self, handler, append: bool = True):
        """
            Update home button handler

            Parameters:
            handler (callable): New handler
            append (bool): True if appending the new handler to the existing handler

            Returns:
            None

        """
        self.ui.hangmanDisplay.setHomeHandler(handler, append)

    def win(self) -> None:
        """
            Process when the user wins the game

            Returns:
            None

        """
        self.ui.hangmanDisplay.showReplayButton()
        self.ui.scoreDisplay.addScore(Score.WIN())

    def lose(self) -> None:
        """
            Process when the user loses the game

            Returns:
            None

        """
        self.ui.hangmanDisplay.showReplayButton()
        self.ui.scoreDisplay.addScore(Score.LOSE())

    def correctGuess(self, duplicate=1) -> None:
        """
            Process when user guess the character correctly. It changes the score

            Parameters:
            duplicate (int): Number of duplicate correct guesses

            Returns:
            None

        """
        self.ui.scoreDisplay.addScore(Score.CORRECT(duplicate))

    def wrongGuess(self) -> None:
        """
            Process when user guess the character wrong. It changes the score

            Returns:
            None

        """
        self.ui.scoreDisplay.addScore(Score.WRONG())

    def setDifficultyHandler(self, handler: callable(Difficulty)):
        """
            Sets the callback function to the difficulty button in Home UI

            Parameters:
            handler (callable): Callback function attached to the difficulty button

            Returns:
            None

        """
        self.difficultyHandler = lambda x: [handler(x), self.ui.difficultyLabel.setText(x.name)]


class Ui(QtWidgets.QWidget):
    def __init__(self, assets_dir="../assets"):
        super(Ui, self).__init__()
        uic.loadUi(assets_dir + '/ui/main_v4.ui', self)
        # self.form_widget.keyboardFirstRowView.layout().addWidget(KeyTop())
        self.keyboard = Keyboard(assets_dir=assets_dir)
        self.wordBox = WordBox(assets_dir=assets_dir)
        self.lifeBox = LifeBox(assets_dir=assets_dir)
        self.hangmanDisplay = HangmanView(assets_dir=assets_dir)
        self.scoreDisplay = ScoreView(assets_dir=assets_dir)
        self.keyboardView.setLayout(QtWidgets.QHBoxLayout())
        self.keyboardView.layout().addWidget(self.keyboard)
        self.wordInputView.setLayout(QtWidgets.QHBoxLayout())
        self.wordInputView.layout().setContentsMargins(0, 0, 0, 0)
        self.wordInputView.layout().addWidget(self.wordBox)
        self.lifeView.setLayout(QtWidgets.QHBoxLayout())
        self.lifeView.layout().setContentsMargins(0, 0, 0, 0)
        self.lifeView.layout().addWidget(self.lifeBox)

        self.hangmanView.setLayout(QtWidgets.QHBoxLayout())
        self.hangmanView.layout().setContentsMargins(0, 0, 0, 0)
        self.hangmanView.layout().addWidget(self.hangmanDisplay)

        self.scoreView.setLayout(QtWidgets.QHBoxLayout())
        self.scoreView.layout().setContentsMargins(0, 0, 0, 0)
        self.scoreView.layout().addWidget(self.scoreDisplay)

        self.hangmanDisplay.setScoreView(self.scoreDisplay)

        # self.lifeBox.setMaxAttempts(7)

    def reset(self):
        self.keyboard.reset()
        self.wordBox.reset()
        self.lifeBox.reset()
        self.scoreDisplay.confirmScore()
        self.hangmanDisplay.reset()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrame()
    app.exec()
