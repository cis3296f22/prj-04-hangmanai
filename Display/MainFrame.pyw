import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import (Qt)

from Display.HangmanView import HangmanView
from Display.Home import Home
from Display.Keyboard import Keyboard
from Display.LifeBox import LifeBox
from Display.ScoreView import ScoreView
from Display.WordBox import WordBox

# Global value for the windows status
from Score import Score
from WordProvider import Difficulty

WINDOW_SIZE = 0


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self,
                 parent=None,
                 keyboard_handler: callable([str, list[str]]) = lambda x, y: print("[" + x + "] -> " + str(y)),
                 difficulty_handler: callable(str) = lambda x: print(x),
                 assets_dir: str = "../assets"):

        super(MainFrame, self).__init__(parent)
        self.assets_dir: str = assets_dir
        self.game = None
        # TODO Word API needed to pass word to guess to hangman
        # self.ui = Ui(assets_dir=assets_dir)
        # self.setCentralWidget(self.ui)
        self.ui: Ui = Ui(assets_dir=self.assets_dir)
        self.ui.hangmanDisplay.setHomeHandler(self.transitHome)
        self.home: Home = Home(buttonHandler=self.transitMainGame, assets_dir=assets_dir)
        self.setCentralWidget(self.home)

        self.keyboard_handler: callable = keyboard_handler
        self.ui.keyboard.setKeyboardListner(keyboard_handler)

        self.difficultyHandler: callable(str) = difficulty_handler

        self.show()
        self.windowInit()

        # self.ui.
    def windowInit(self):
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

    def setDifficultyHandler(self, handler: callable(str)):
        self.difficultyHandler = handler

    def transitMainGame(self, args=None):
        self.difficultyHandler(args)
        self.home = self.takeCentralWidget()
        self.setCentralWidget(self.ui)
        self.windowInit()

    def transitHome(self, args=None):
        self.ui = self.takeCentralWidget()
        self.setCentralWidget(self.home)
        self.windowInit()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    # Restore or maximize your window
    def restore_or_maximize_window(self):

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

    def setKeyListner(self, key, handler, append=False):
        self.ui.keyboard.setKeyListner(key, handler, append)

    def setKeyboardListner(self, handler, append=False):
        self.ui.keyboard.setKeyboardListner(handler, append)

    def reset(self):
        self.ui.keyboard.reset()
        self.ui.wordBox.reset()

    def hideWord(self):
        self.ui.wordBox.hideWord()

    def hideCharAt(self, index):
        self.ui.wordBox.hideCharAt(index)

    def showWord(self):
        self.ui.wordBox.showWord()

    def showCharAt(self, index):
        self.ui.wordBox.showCharAt(index)

    def wrongChars(self):
        self.ui.wordBox.wrongChars()

    def wrongCharAt(self, index):
        self.ui.wordBox.wrongCharAt(index)

    def setWord(self, word, hide=False):
        self.ui.wordBox.setWord(word, hide)

    def setCharacterAt(self, index, char):
        self.ui.wordBox.setCharacterAt(index, char)

    def setMaxAttempts(self, max_attempts):
        self.ui.lifeBox.setMaxAttempts(max_attempts)
        self.ui.hangmanDisplay.setMaxAttempts(max_attempts)

    def setLife(self, number):
        life = self.ui.lifeBox.getLife()
        self.ui.lifeBox.setLife(number)
        if life > number:
            self.ui.hangmanDisplay.takeDamage()

    def takeLife(self, zeroHandler):

        life = self.ui.lifeBox.getLife()
        if life > 0:
            self.ui.hangmanDisplay.takeDamage()
        self.ui.lifeBox.takeLife(zeroHandler)

    def setReplayHandler(self, handler, append: bool = True):
        self.ui.hangmanDisplay.setReplayHandler(handler, append)

    def setHomeHandler(self, handler, append: bool = True):
        self.ui.hangmanDisplay.setHomeHandler(handler, append)

    def win(self):
        self.ui.hangmanDisplay.showReplayButton()
        self.ui.scoreDisplay.addScore(Score.WIN())

    def lose(self):
        self.ui.hangmanDisplay.showReplayButton()
        self.ui.scoreDisplay.addScore(Score.LOSE())

    def correctGuess(self, duplicate=1):
        self.ui.scoreDisplay.addScore(Score.CORRECT(duplicate))

    def wrongGuess(self):
        self.ui.scoreDisplay.addScore(Score.WRONG())

    def setDifficultyHandler(self, handler: callable(Difficulty)):
        self.difficultyHandler = lambda x:   [handler(x), self.ui.difficultyLabel.setText(x.name)]

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
        self.hangmanDisplay.setReplayHandler(lambda: [self.keyboard.reset(),
                                                      self.wordBox.reset(),
                                                      self.lifeBox.reset(),
                                                      self.scoreDisplay.confirmScore(),
                                                      self.hangmanDisplay.reset()])
        self.hangmanDisplay.setHomeHandler(lambda: [self.keyboard.reset(),
                                                      self.wordBox.reset(),
                                                      self.lifeBox.reset(),
                                                      self.scoreDisplay.confirmScore(),
                                                      self.hangmanDisplay.reset()])
        self.scoreView.setLayout(QtWidgets.QHBoxLayout())
        self.scoreView.layout().setContentsMargins(0, 0, 0, 0)
        self.scoreView.layout().addWidget(self.scoreDisplay)

        self.hangmanDisplay.setScoreView(self.scoreDisplay)

        # self.lifeBox.setMaxAttempts(7)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrame()
    app.exec()
