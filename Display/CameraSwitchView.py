import sys

from PyQt6 import QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import (QPoint, QRect,
                          QTimer, QUrl)
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygon, QFont
from PyQt6.QtMultimedia import QSoundEffect

from Display.ScoreView import ScoreView
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


class CameraSwitchView(QtWidgets.QWidget):
    def __init__(self,
                 max_attempts: int = 5,
                 progress: float = 0,
                 assets_dir: str = "../assets",
                 reply_handler=lambda: print("Replay!!"),
                 home_handler=lambda: print("Home!!"),
                 debug_anim: bool = False):
        super(CameraSwitchView, self).__init__()

        uic.loadUi(assets_dir + '/ui/hangmanView.ui', self)
        self.assets_dir: str = assets_dir

    def paintEvent(self, e) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        regionRect: QRectF = self.getHangmanRect()

        if self.scoreView is not None:
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

        # painter.drawRect(socreFeedRect.toRect())

        score_feed = self.scoreView.getFeed()
        for i in range(0, len(score_feed)):
            score = score_feed[i]
            rect = self.getButtonRect(socreFeedRect.left(),
                                      socreFeedRect.top(),
                                      socreFeedRect.width(),
                                      socreFeedRect.height(), 0.5, 0.1, (i + 1) * socreFeedRect.height() * 0.12)

            length = rect.height() if rect.height() < rect.width() else rect.width()
            corner_radius = int(length) / 2

            painter.setPen(score.getPen(int(255 * (5 - i) / 5)))
            painter.setBrush(score.getBGColor(int(255 * (5 - i) / 5)))

            painter.drawRoundedRect(rect, corner_radius, corner_radius)

            painter.setFont(QFont("Consolas", self.fontSize(str(score), rect.width(), rect.height(), 0.65)))
            painter.setPen(QPen(QColor(255, 255, 255, int(255 * (5 - i) / 5)), 0))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(score))

    def wordWidth(self, word: str, fontSize: float) -> float:
        slope = 0.7331 * fontSize - 0.0438
        intercept = -0.0729 * fontSize + 0.1588
        return len(word) * slope + intercept

    def fontSize(self, word: str, availableWidth: float, availableHeight: float, marginRatio: float = 1) -> int:
        widthForHeight = self.wordWidth(word, availableHeight * marginRatio * 3 / 4)
        if widthForHeight > availableWidth * marginRatio:
            return int(self.fontSizeForWidth(word, availableWidth * marginRatio))
        return int(availableHeight * marginRatio * 3 / 4)

    def fontSizeForWidth(self, word: str, width: float) -> int:
        return int((width + 0.0438 * len(word) - 0.1588) / (len(word) * 0.7331 - 0.1))  # 0.0729

    def getButtonRect(self, left: int, top: int, width: int, height: int,
                      width_ratio: float, height_ratio: float, shift_y: float) -> QRectF:
        center = QPointF(left + 0.5 * width, top + shift_y)
        size = QPointF(width * width_ratio, height * height_ratio)
        return QRectF(
            (center - size / 2),
            (center + size / 2)
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
