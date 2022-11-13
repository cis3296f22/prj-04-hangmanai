import PyQt6.QtMultimedia
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import pyqtProperty, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)
import sys
from GUI.LifeCircle import LifeCircle
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt

SOUND_FILE = "sound/knife.wav"

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = HangmanView(progress=1, debug_anim=True)
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class HangmanView(QtWidgets.QWidget):
    def __init__(self, max_attempts: int = 5, progress: float = 0, assets_dir: str = "../assets", debug_anim: bool = False):
        super(HangmanView, self).__init__()
        uic.loadUi(assets_dir + '/ui/hangmanView.ui', self)
        self.assets_dir: str = assets_dir

        self.thicknessRatio: float = 0.05
        self.thickness: int = 1
        self.progress_percentage: float = progress
        self.max_attempts: int = max_attempts
        self.attempts: int = self.max_attempts
        self.debug_anim: bool = debug_anim

        self.drawings = [
            self.drawBase,
            self.drawPoll,
            self.drawSupport,
            self.drawTop,
            self.drawHanger,
            self.drawHead,
            self.drawBody,
            self.drawLeftArm,
            self.drawRightArm,
            self.drawLeftLeg,
            self.drawRightLeg
        ]
        self.value: float = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.animTest())
        self.effect = None



    def tageDamage(self)-> None:
        filename = self.assets_dir + "/" + SOUND_FILE
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(filename))
        self.effect.play()

        self.value = 1
        self.timer.start(10)
        if self.attempts <= 0:
            print("Hangman animation cannot got beyond")
            return
        self.attempts = self.attempts - 1
        if self.attempts == 0:
            self.setStageProgress(1)
        else:
            self.setStageProgress((self.max_attempts - self.attempts) / self.max_attempts)


    def setMaxAttempts(self, max_attempts: int) -> None:
        print("Changed max attempts (Hangman View) -> " + str(max_attempts))
        self.max_attempts = max_attempts
        self.attempts = max_attempts

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.debug_anim:
            self.tageDamage()
            self.reset()
            self.progress_percentage = 1

    def animTest(self):
        self.value -= 0.1
        if self.value < 0:
            self.value = 1
            self.timer.stop()
        else:
            self.repaint()

    def setStageProgress(self, progress_percentage: float) -> None:
        self.progress_percentage = progress_percentage
        print("Changed max progress (Hangman View) -> " + str(progress_percentage))

    def reset(self):
        self.attempts = self.max_attempts

    def paintEvent(self, e) -> None:

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
        # qp.setBrush(QColor(int(29 * self.value), int(27 * self.value), int(24 * self.value)))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        rect = QtCore.QRect(left, top, width32, height32)
        qp.drawRect(rect)


        # self.drawBase(qp, QColor(100, 100, 100), left, top, width32, height32)
        # self.drawSupport(qp, QColor(100, 100, 100), left, top, width32, height32)
        # self.drawPoll(qp, QColor(100, 100, 100), left, top, width32, height32)
        # self.drawTop(qp, QColor(100, 100, 100), left, top, width32, height32)
        # self.drawHanger(qp, QColor(100, 100, 100), left, top, width32, height32)
        #
        # self.drawHead(qp, QColor(255, 255, 255), left, top, width32, height32)
        # self.drawBody(qp, QColor(255, 255, 255), left, top, width32, height32)
        # self.drawLeftArm(qp, QColor(255, 255, 255), left, top, width32, height32)
        # self.drawRightArm(qp, QColor(255, 255, 255), left, top, width32, height32)
        # self.drawLeftLeg(qp, QColor(255, 255, 255), left, top, width32, height32)
        # self.drawRightLeg(qp, QColor(255, 255, 255), left, top, width32, height32)

        for i in range(len(self.drawings)):
            if self.progress_percentage <= i / len(self.drawings):
                break
            if i == (len(self.drawings) - 1) and self.progress_percentage != 1:
                break

            # color = QColor(100, 100, 100) if i < 5 else QColor(255, 255, 255)
            color = QColor(
                    100 + int((255 - 100) * self.value),
                    100 + int((255 - 100) * self.value),
                    100 + int((255 - 100) * self.value)) if i < 5 else QColor(
                                                                    255,
                                                                    255 - int(255 * self.value),
                                                                    255 - int(255 * self.value))

            self.drawings[i](qp, color, left, top, width32, height32)

        qp.end()


    def drawBase(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
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

    def drawPoll(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
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

    def drawTop(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
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

    def drawSupport(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        painter.setBrush(color)
        painter.drawPolygon(
            QtGui.QPolygon([
                QPoint(left + int(width * 0.4), top + int(height * 0.2)),
                QPoint(left + int(width * 0.4) + self.thickness, top + int(height * 0.2)),
                QPoint(left + int(width * 0.2), top + int(height * 0.4) + self.thickness),
                QPoint(left + int(width * 0.2), top + int(height * 0.4))
            ]))

    def drawHanger(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        pen.setWidth(self.thickness // 2)
        painter.setPen(pen)

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.2))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        painter.drawLine(start, end)

    def drawHead(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))
        painter.setBrush(color)

        radius = int(self.thickness * 1.5)
        center = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))

        painter.drawEllipse(center, radius, radius)

    def drawBody(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        painter.drawLine(start, end)

    def drawLeftArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawRightArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawLeftLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def drawRightLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def initPen(self, pen: QPen) -> QPen:
        pen.setWidth(self.thickness // 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        return pen

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
