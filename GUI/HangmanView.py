from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)
import sys
from GUI.LifeCircle import LifeCircle
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = HangmanView()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class HangmanView(QtWidgets.QWidget):
    def __init__(self, assets_dir="../assets"):
        super(HangmanView, self).__init__()
        uic.loadUi(assets_dir + '/ui/hangmanView.ui', self)
        self.assets_dir = assets_dir

    def paintEvent(self, e):
        # super().paintEvent(e)
        print("Painting")
        qp = QtGui.QPainter()
        qp.begin(self)
        # qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(e.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "Sample")

        width = qp.device().width()
        height = qp.device().height()
        width_ratio = 2
        height_ratio = 3

        width32 = None
        height32 = None
        top = None
        left = None
        if width * height_ratio / width_ratio < height:
            width32 = width
            height32 = width * height_ratio / width_ratio
            top = (height - height32) / 2
            left = 0

        else:
            height32 = height
            width32 = height32 * width_ratio / height_ratio
            top = 0
            left = (width - width32) / 2

        width32 = int(width32)
        height32 = int(height32)
        top = int(top)
        left = int(left)
        rect = QtCore.QRect(left, top, width32, height32)
        qp.setBrush(QColor(100, 100, 0))
        qp.drawRect(rect)
        # qp.fillRect(rect, Qt.BrushStyle.SolidPattern)


        positionBottomBar = (
            left,
            top + int(height32 * 0.9),
            width32,
            int(height32 * 0.05)
        )
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(
            positionBottomBar[0],
            positionBottomBar[1],
            positionBottomBar[2],
            positionBottomBar[3])

        positionPoll = (
            left + int(width32 * 0.2),
            top + int(height32 * 0.1),
            int(width32 * 0.05),
            int(height32 * 0.8)
        )
        qp.drawRect(
            positionPoll[0],
            positionPoll[1],
            positionPoll[2],
            positionPoll[3])

        positionTopBar = (
            left + int(width32 * 0.1),
            top + int(height32 * 0.2),
            int(width32 * 0.8),
            int(height32 * 0.05)
        )
        qp.drawRect(
            positionTopBar[0],
            positionTopBar[1],
            positionTopBar[2],
            positionTopBar[3])

        # pen = QPen(Qt.GlobalColor.white, int(height32 * 0.05), Qt.PenStyle.SolidLine)
        #
        # qp.setPen(pen)
        #
        # positionSupportBar = (
        #     left + int(width32 * 0.2),
        #     top + int(height32 * 0.4),
        #     left + int(width32 * 0.4),
        #     top + int(height32 * 0.2),
        # )
        # qp.drawLine(
        #     positionSupportBar[0],
        #     positionSupportBar[1],
        #     positionSupportBar[2],
        #     positionSupportBar[3])

        qp.drawPolygon(
            QtGui.QPolygon([
                QPoint(left + int(width32 * 0.4), top + int(height32 * 0.2),),
                QPoint(left + int(width32 * 0.5), top + int(height32 * 0.2), ),
                QPoint(left + int(width32 * 0.2), top + int(height32 * 0.5), ),
                QPoint(left + int(width32 * 0.2), top + int(height32 * 0.4) )
            ]))

        qp.end()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()