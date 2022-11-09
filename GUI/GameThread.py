from PyQt6.QtCore import Qt, QObject, QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys
from MainFrame import MainFrame
import threading

class GameThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Thread creation")

    def run(self):
        print("running")

def appCreation(app):
    print("a")

    app.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainFrame()
    widget.show()
    thread1 = threading.Thread(target=lambda:appCreation(app))
    thread1.start()
    print("App created")
