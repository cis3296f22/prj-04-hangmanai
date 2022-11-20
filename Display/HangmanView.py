import math

from PyQt6 import uic
import sys

from PyQt6 import QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import (QPoint, QRect,
                          QTimer, QUrl)
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygon, QFont, QFontMetrics
from PyQt6.QtMultimedia import QSoundEffect

from Score import Score

SOUND_FILE = "sound/knife.wav"


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = HangmanView(progress=1, debug_anim=True)
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.form_widget.showReplayButton(5)
        self.show()


class HangmanView(QtWidgets.QWidget):
    def __init__(self,
                 max_attempts: int = 5,
                 progress: float = 0,
                 assets_dir: str = "../assets",
                 reply_handler=lambda: print("Replay!!"),
                 home_handler=lambda: print("Home!!"),
                 debug_anim: bool = False):
        super(HangmanView, self).__init__()

        uic.loadUi(assets_dir + '/ui/hangmanView.ui', self)
        self.assets_dir: str = assets_dir

        self.thicknessRatio: float = 0.05
        self.thickness: int = 1
        self.progress_percentage: float = progress
        self.max_attempts: int = max_attempts
        self.attempts: int = self.max_attempts
        self.debug_anim: bool = debug_anim
        self.reply_handler = reply_handler
        self.home_handler = home_handler
        self.score_feed: list[Score] = []

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
        self.damageAnimValue: float = 0
        self.damageTimer = QTimer()
        self.damageTimer.timeout.connect(lambda: self.damageAnim())
        self.effect = None
        self.overlay: float = 1
        self.overlayTimer = QTimer()
        self.overlayTimer.timeout.connect(lambda: self.overlayAnim())
        # self.showReplayButton(5)

    def updateScoreFeed(self):
        print("Update score feed")


    def showReplayButton(self, duration: int = 5) -> None:
        self.overlayTimer.start(duration)

    def hideReplayButton(self) -> None:
        self.overlayTimer.stop()
        self.overlay = 1

    def startDamageAnimation(self, duration: int = 5):
        self.damageAnimValue = 1
        self.damageTimer.start(duration)

    def takeDamage(self) -> None:
        filename = self.assets_dir + "/" + SOUND_FILE
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(filename))
        self.effect.play()

        self.startDamageAnimation(5)

        if self.attempts <= 0:
            print("Hangman animation cannot got beyond")
            return
        self.attempts = self.attempts - 1
        if self.attempts == 0:
            self.setStageProgress(1)
        else:
            self.setStageProgress((self.max_attempts - self.attempts) / self.max_attempts)

    def setReplayHandler(self, handler, append: bool = True):
        func = self.reply_handler
        if self.reply_handler is not None and append:
            self.reply_handler = lambda: [func(), handler()]
        else:
            self.reply_handler = lambda: handler()

    def setHomeHandler(self, handler, append: bool = True):
        func = self.home_handler
        if self.home_handler is not None and append:
            self.home_handler = lambda: [func(), handler()]
        else:
            self.home_handler = lambda: handler()

    def setStageProgress(self, progress_percentage: float) -> None:
        self.progress_percentage = progress_percentage

    def setMaxAttempts(self, max_attempts: int) -> None:
        self.max_attempts = max_attempts
        self.attempts = max_attempts

    def reset(self):
        self.attempts = self.max_attempts
        self.overlay = 1
        self.damageAnimValue = 0
        self.setStageProgress(0)
        self.repaint()
        self.damageTimer.stop()
        self.overlayTimer.stop()
        # self.showReplayButton(5)

    def overlayAnim(self) -> None:
        # if self.overlay < 0.5:
        #     self.overlay = 1

        if self.overlay < 0.5:
            self.overlayTimer.stop()
        else:
            self.overlay -= 0.01
            self.repaint()


    def damageAnim(self):
        if self.damageAnimValue <= 0:
            self.damageAnimValue = 1
        self.damageAnimValue -= 0.05
        if self.damageAnimValue < 0:
            self.damageTimer.stop()
        else:
            self.repaint()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.debug_anim:
            self.takeDamage()
            self.attempts = self.max_attempts
            self.progress_percentage = 1
        rect = self.getHangmanRect()

        # Reply
        if self.getReplyButtonRect(
                rect.left(), rect.top(), rect.width(), rect.height()
        ).contains(event.position()) and self.overlay != 1:
            if self.reply_handler is not None:
                self.reply_handler()

        # Home button
        if self.getHomeRect(
                rect.left(), rect.top(), rect.width(), rect.height()
        ).contains(event.position()) and self.overlay != 1:
            if self.home_handler is not None:
                self.home_handler()

    def getHangmanRect(self) -> QRectF:
        width = self.width()
        height = self.height()
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

        rect = QRectF(left, top, width32, height32)
        return rect

    def getScoreFeedRect(self, hangmanRect: QRectF) -> QRectF:
        width: int = self.width()
        leftSpacingWidth = int((width - hangmanRect.width()) / 2)

        return QRectF(self.width() // 2 + int(hangmanRect.width() / 2), 0, leftSpacingWidth, self.height())


    def paintEvent(self, e) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        regionRect: QRectF = self.getHangmanRect()

        self.drawScoreFeed(qp, regionRect)
        self.thickness = int(self.thicknessRatio * regionRect.width())

        qp.setBrush(QColor(29, 27, 24))
        # qp.setBrush(QColor(int(29 * self.value), int(27 * self.value), int(24 * self.value)))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        rect = regionRect.toRect()
        qp.drawRect(rect)

        for i in range(len(self.drawings)):
            if self.progress_percentage <= i / len(self.drawings):
                break
            if i == (len(self.drawings) - 1) and self.progress_percentage != 1:
                break

            color = QColor(
                    int((100 + int((255 - 100) * self.damageAnimValue)) * self.overlay),
                    int((100 + int((255 - 100) * self.damageAnimValue)) * self.overlay),
                    int((100 + int((255 - 100) * self.damageAnimValue)) * self.overlay)
            ) if i < 5 else QColor(
                                int(255 * self.overlay),
                                int((255 - int(255 * self.damageAnimValue)) * self.overlay),
                                int((255 - int(255 * self.damageAnimValue)) * self.overlay))

            self.drawings[i](qp, color, rect.left(), rect.top(), rect.width(), rect.height())
        # self.overlay = 0.5
        self.drawReplayButton(qp, QColor(66, 205, 82), rect.left(), rect.top(), rect.width(), rect.height())
        self.drawHomeButton(qp, QColor(66, 205, 82), rect.left(), rect.top(), rect.width(), rect.height())
        qp.end()

    def drawScoreFeed(self, painter: QPainter, hangmanRect: QRectF) -> None:
        painter.setBrush(QColor(255, 27, 24))
        socreFeedRect = self.getScoreFeedRect(hangmanRect)

        painter.drawRect(socreFeedRect.toRect())

        for i in range(0, 5):
            rect = self.getButtonRect(socreFeedRect.left(),
                                      socreFeedRect.top(),
                                      socreFeedRect.width(),
                                      socreFeedRect.height(), 0.5, 0.1, (i + 1) * socreFeedRect.height() * 0.12)

            length = rect.height() if rect.height() < rect.width() else rect.width()
            corner_radius = int(length) / 2
            painter.drawRoundedRect(rect, corner_radius, corner_radius)
            # fm = painter.fontMetrics()
            # fm = QFontMetrics(QFont("Consolas", 1))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 2))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 4))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 8))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 16))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 32))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 64))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 128))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 256))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 512))
            # print(fm.boundingRect("123").width())
            # fm = QFontMetrics(QFont("Consolas", 1024))
            # print(fm.boundingRect("123").width())
            #
            # word = "12345"
            # fontSize = 45
            # fm = QFontMetrics(QFont("Consolas", fontSize))
            # print("actual width -> " + str(fm.boundingRect(word).width()))
            # print("calcul width -> " + str(self.wordWidth(word, fontSize)))
            #
            # word = "12345"
            # width = 250
            # fontSize = self.fontSizeForWidth(word, width)
            # fm = QFontMetrics(QFont("Consolas", fontSize))
            # print("actual width -> " + str(fm.boundingRect(word).width()))
            # print("calcul width -> " + str(self.wordWidth(word, fontSize)))
            #
            #
            # # for power in range(10):
            # #     print("Pow" + str(math.pow(2, power)))
            # #     fm = QFontMetrics(QFont("Consolas", math.pow(2, power)))
            # #     for i in range(20):
            # #         print(fm.boundingRect("".join([str(x % 10) for x in range(i + 1)])).width())
            #



            painter.setFont(QFont("Consolas", int(self.fontSize(rect.width(), rect.height(), "Sample"))))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Sample")
            font = painter.font()
            ps = font
            # print(str(ps.toString()))

            # print(painter.fontMetrics().height())
    def wordWidth(self, word, fontSize):
        slope = 0.7331 * fontSize - 0.0438
        intercept = -0.0729 * fontSize + 0.1588
        return len(word) * slope + intercept

    def fontSize(self, availableWidth, availableHeight, word):
        widthForHeight = self.wordWidth(word, availableHeight * 3 / 4)
        if widthForHeight > availableWidth:
            return self.fontSizeForWidth(word, availableWidth)
        return availableHeight * 3 / 4

    def fontSizeForWidth(self, word, width):
        return (width + 0.0438 * len(word) - 0.1588) / (len(word) * 0.7331 - 0.1) # 0.0729

    def getButtonRect(self, left: int, top: int, width: int, height: int,
                      width_ratio: float, height_ratio: float, shift_y: float) -> QRectF:
        center = QPointF(left + 0.5 * width, top + shift_y)
        size = QPointF(width * width_ratio, height * height_ratio)
        return QRectF(
            (center - size / 2),
            (center + size / 2)
        )

    def getHomeRect(self, left: int, top: int, width: int, height: int) -> QRectF:
        return self.getButtonRect(left, top, width, height, 0.8, 0.2, 0.7 * height)

    def drawHomeButton(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        color.setAlpha(int(255 * ((1 - self.overlay) * 2)))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.setPen(pen)

        center = self.getHomeRect(left, top, width, height).center()
        size = self.getReplyButtonSize(left, top, width, height)
        rect = self.getHomeRect(left, top, width, height).toRect()

        length = size.y() if size.y() < size.x() else size.x()
        corner_radius = int(length) / 2
        painter.drawRoundedRect(rect, corner_radius, corner_radius)
        color_icon = QColor(255, 255, 255, int(255 * ((1 - self.overlay) * 2)))
        pen = QPen(color_icon)
        pen.setWidth(int(height * 0.1 / 8))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        size_icon: QPointF = QPointF(length, length) / 24 * 9

        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        painter.setPen(pen)
        painter.setBrush(color_icon)
        size_triangle = size_icon
        triangle = QPolygon([
            QPointF(center.x() - size_triangle.x(), center.y() + size_triangle.y() * 1 / 2).toPoint(),
            QPointF(center.x(), center.y() - size_triangle.y() * 1 / 3).toPoint(),
            QPointF(center.x() + size_triangle.x(), center.y() + size_triangle.y() * 1 / 2).toPoint()]
        ).translated(0, - (size_icon.toPoint() / 3 * 2).y())
        painter.drawPolygon(triangle, Qt.FillRule.WindingFill)

        rect = QRect(
            (center - size_icon / 2).toPoint(),
            (center + size_icon / 2).toPoint()
        ).translated(0, (size_icon / 4).toPoint().y())
        painter.drawRect(rect)

    def getReplyButtonRect(self, left: int, top: int, width: int, height: int) -> QRectF:
        return self.getButtonRect(left, top, width, height, 0.8, 0.2, 0.3 * height)

    def getReplyButtonPosition(self, left: int, top: int, width: int, height: int) -> QPointF:
        return self.getReplyButtonRect(left, top, width, height).center()

    def getReplyButtonSize(self, left: int, top: int, width: int, height: int) -> QPointF:
        rect = self.getReplyButtonRect(left, top, width, height)
        return rect.bottomRight() - rect.topLeft()

    def drawReplayButton(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        color.setAlpha(int(255 * ((1 - self.overlay) * 2)))
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.setPen(pen)

        center = self.getReplyButtonPosition(left, top, width, height)
        size = self.getReplyButtonSize(left, top, width, height)
        rect = self.getReplyButtonRect(left, top, width, height).toRect()

        length = size.y() if size.y() < size.x() else size.x()
        corner_radius = int(length) / 2
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

        color_icon = QColor(255, 255, 255, int(255 * ((1 - self.overlay) * 2)))
        startAngle = 0 * 16
        spanAngle = -270 * 16
        pen = QPen(color_icon)
        pen.setWidth(int(height * 0.2 / 8))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        size_arc = QPointF(length, length) / 7 * 2
        arc_rect = QRect(
            (center - size_arc).toPoint(),
            (center + size_arc).toPoint()
        )
        painter.drawArc(arc_rect, startAngle, spanAngle)

        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        painter.setPen(pen)
        painter.setBrush(color_icon)
        size_triangle = size_arc
        triangle = QPolygon([
            QPointF(center.x() - size_triangle.x() * 1 / 3, center.y() - size_triangle.y() / 2).toPoint(),
            QPointF(center.x() + size_triangle.x() * 2 / 3, center.y()).toPoint(),
            QPointF(center.x() - size_triangle.x() * 1 / 3, center.y() + size_triangle.y() / 2).toPoint()]
        ).translated(0, - size_arc.toPoint().y())
        painter.drawPolygon(triangle, Qt.FillRule.WindingFill)


    def drawBase(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        painter.setBrush(color)
        positionBottomBar = (
            left,
            top + height - self.thickness,
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
            int(height * 0.9)
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
