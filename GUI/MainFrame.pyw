from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys

from GUI.Keyboard import Keyboard
from GUI.WordBox import WordBox

# Global value for the windows status
WINDOW_SIZE = 0


class MainFrame(QtWidgets.QMainWindow):
    def __init__(self, parent=None,  handler=lambda x: print("Keyboard handler [" + x + "]"), assets_dir="../assets"):

        super(MainFrame, self).__init__(parent)
        self.game = None
        # TODO Word API needed to pass word to guess to hangman
        self.ui = Ui(assets_dir=assets_dir)
        self.setCentralWidget(self.ui)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()

        # Button click events to our top bar buttons
        #
        # Minimize window
        if hasattr(self.ui, "minimizeButton"):
            self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        # Close window
        if hasattr(self.ui, "closeButton"):
            self.ui.closeButton.clicked.connect(lambda: self.close())
        # Restore/Maximize window
        if hasattr(self.ui, "restoreButton"):
            self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())

        def moveWindow(event):
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        if hasattr(self.ui, "title_bar"):
            # Remove window tlttle bar
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

            # Set main background to transparent
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
            if hasattr(self.ui, "title_bar"):
                self.ui.title_bar.mouseMoveEvent = moveWindow

        self.ui.keyboard.setKeyboardListner(handler)

        # Show window
        self.show()

        # self.ui.

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

    def blank(self):
        self.ui.wordBox.blank()

    def blankAt(self, index):
        self.ui.wordBox.blankAt(index)

    def setWord(self, word):
        self.ui.wordBox.setWord(word)

    def setCharacterAt(self, index, char):
        self.ui.wordBox.setCharacterAt(index, char)

    # TODO setRemainingAttempts
    def setRemainingAttempts(self, number):
        print("TODO setRemainingAttempts(" + number + ")")

    # TODO getRemainingAttempts
    def getRemainingAttempts(self, number):
        print("TODO getRemainingAttempts()")

    # TODO win
    def win(self):
        print("TODO win()")

    # TODO lose
    def lose(self):
        print("TODO lose()")

    def setGame(self, game):
        self.game = game

class Ui(QtWidgets.QWidget):
    def __init__(self, assets_dir="../assets"):
        super(Ui, self).__init__()
        uic.loadUi(assets_dir + '/ui/main.ui', self)
        # self.form_widget.keyboardFirstRowView.layout().addWidget(KeyTop())
        self.keyboard = Keyboard(assets_dir=assets_dir)
        self.wordBox = WordBox(assets_dir=assets_dir)
        self.keyboardView.setLayout(QtWidgets.QHBoxLayout())
        self.keyboardView.layout().addWidget(self.keyboard)
        self.wordInputView.setLayout(QtWidgets.QHBoxLayout())
        self.wordInputView.layout().setContentsMargins(0, 0, 0, 0)
        self.wordInputView.layout().addWidget(self.wordBox)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrame()
    app.exec()
