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

        self.thicknessRatio = 0.05
        self.thickness = self.thicknessRatio * 0

    def paintEvent(self, e):


        qp = QtGui.QPainter()
        qp.begin(self)

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

        self.thickness = int(self.thicknessRatio * width32)


        qp.setBrush(QColor(29, 27, 24))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        rect = QtCore.QRect(left, top, width32, height32)
        qp.drawRect(rect)


        self.drawBase(qp, QColor(100, 100, 100), left, top, width32, height32)
        self.drawSupport(qp, QColor(100, 100, 100), left, top, width32, height32)
        self.drawPoll(qp, QColor(100, 100, 100), left, top, width32, height32)
        self.drawTop(qp, QColor(100, 100, 100), left, top, width32, height32)
        self.drawHanger(qp, QColor(100, 100, 100), left, top, width32, height32)

        self.drawHead(qp, QColor(255, 255, 255), left, top, width32, height32)
        self.drawBody(qp, QColor(255, 255, 255), left, top, width32, height32)
        self.drawLeftArm(qp, QColor(255, 255, 255), left, top, width32, height32)
        self.drawRightArm(qp, QColor(255, 255, 255), left, top, width32, height32)
        self.drawLeftLeg(qp, QColor(255, 255, 255), left, top, width32, height32)
        self.drawRightLeg(qp, QColor(255, 255, 255), left, top, width32, height32)

        qp.end()


    def drawBase(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        # brush = QtGui.QBrush(QColor(255, 255, 255))
        # brush.setStyle(Qt.BrushStyle.Dense6Pattern)
        painter.setBrush(color)
        positionBottomBar = (
            left,
            top + int(height * 0.9),
            width,
            self.thickness
        )

        painter.drawRect(
            positionBottomBar[0],
            positionBottomBar[1],
            positionBottomBar[2],
            positionBottomBar[3])

    def drawPoll(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        painter.setBrush(color)
        positionPoll = (
            left + int(width * 0.2),
            top + int(height * 0.1),
            self.thickness,
            int(height * 0.8)
        )
        painter.drawRect(
            positionPoll[0],
            positionPoll[1],
            positionPoll[2],
            positionPoll[3])

    def drawTop(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        painter.setBrush(color)
        positionTopBar = (
            left + int(width * 0.1),
            top + int(height * 0.2),
            int(width * 0.8),
            self.thickness
        )
        painter.drawRect(
            positionTopBar[0],
            positionTopBar[1],
            positionTopBar[2],
            positionTopBar[3])

    def drawSupport(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        painter.setBrush(color)
        painter.drawPolygon(
            QtGui.QPolygon([
                QPoint(left + int(width * 0.4), top + int(height * 0.2)),
                QPoint(left + int(width * 0.4) + self.thickness, top + int(height * 0.2)),
                QPoint(left + int(width * 0.2), top + int(height * 0.4) + self.thickness),
                QPoint(left + int(width * 0.2), top + int(height * 0.4))
            ]))

    def drawHanger(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        pen.setWidth(self.thickness // 2)
        painter.setPen(pen)

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.2))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        painter.drawLine(start, end)

    def drawHead(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))
        painter.setBrush(color)

        radius = int(self.thickness * 1.5)
        center = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))

        painter.drawEllipse(center, radius, radius)

    def drawBody(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        painter.drawLine(start, end)

    def drawLeftArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawRightArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawLeftLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def drawRightLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int):
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def initPen(self, pen: QPen):
        pen.setWidth(self.thickness // 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        return pen

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()