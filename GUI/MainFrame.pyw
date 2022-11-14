from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys

from GUI.HangmanView import HangmanView
from GUI.Home import Home
from GUI.Keyboard import Keyboard
from GUI.WordBox import WordBox
from GUI.LifeBox import LifeBox

# Global value for the windows status
WINDOW_SIZE = 0


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self,
                 parent=None,
                 handler: callable([str, list[str]]) = lambda x, y: print("[" + x + "] -> " + str(y)),
                 assets_dir="../assets"):

        super(MainFrame, self).__init__(parent)
        self.assets_dir = assets_dir
        self.game = None
        # TODO Word API needed to pass word to guess to hangman
        # self.ui = Ui(assets_dir=assets_dir)
        # self.setCentralWidget(self.ui)
        self.ui = Ui(assets_dir=self.assets_dir)
        self.home = Home(assets_dir=assets_dir, buttonHandler=self.transitMainGame)
        self.setCentralWidget(self.home)

        self.handler = handler
        self.ui.keyboard.setKeyboardListner(handler)

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


    def transitMainGame(self):
        self.setCentralWidget(self.ui)
        self.windowInit()

    def transitHome(self):
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

    def setWord(self, word, hide=False):
        self.ui.wordBox.setWord(word, hide)

    def setCharacterAt(self, index, char):
        self.ui.wordBox.setCharacterAt(index, char)

    # TODO setRemainingAttempts
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

    # TODO win
    def win(self):
        self.ui.hangmanDisplay.showReplayButton()

    # TODO lose
    def lose(self):
        self.ui.hangmanDisplay.showReplayButton()

    def setGame(self, game):
        self.game = game

class Ui(QtWidgets.QWidget):
    def __init__(self, assets_dir="../assets"):
        super(Ui, self).__init__()
        uic.loadUi(assets_dir + '/ui/main_v3.ui', self)
        # self.form_widget.keyboardFirstRowView.layout().addWidget(KeyTop())
        self.keyboard = Keyboard(assets_dir=assets_dir)
        self.wordBox = WordBox(assets_dir=assets_dir)
        self.lifeBox = LifeBox(assets_dir=assets_dir)
        self.hangmanDisplay = HangmanView(assets_dir=assets_dir)
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
                                                      self.hangmanDisplay.reset()])
        # self.lifeBox.setMaxAttempts(7)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrame()
    app.exec()
