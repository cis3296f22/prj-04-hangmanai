from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys

from Keyboard import Keyboard
from WordBox import WordBox

# Global value for the windows status
WINDOW_SIZE = 0


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui()
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


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../assets/ui/main.ui', self)
        # self.form_widget.keyboardFirstRowView.layout().addWidget(KeyTop())
        self.keyboard = Keyboard()
        self.wordBox = WordBox()
        self.keyboardView.setLayout(QtWidgets.QHBoxLayout())
        self.keyboardView.layout().addWidget(self.keyboard)
        self.wordInputView.setLayout(QtWidgets.QHBoxLayout())
        self.wordInputView.layout().setContentsMargins(0, 0, 0, 0)
        self.wordInputView.layout().addWidget(self.wordBox)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyMainWindow()
    app.exec()
