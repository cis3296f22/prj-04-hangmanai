import sys

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6 import uic
from PyQt6.QtCore import (QPoint, QRect,
                          QTimer, QUrl)
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygon, QFont
from PyQt6.QtMultimedia import QSoundEffect

from Display.Button import Button
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


class HangmanView(QtWidgets.QWidget):
    """
        Hangman Drawing View that is responsible for drawing hangman animation with its progress animation.

    """

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
        """ Path to asset directory"""

        self.thicknessRatio: float = 0.05
        """ Thickness ration for the pen to the width"""
        self.thickness: int = 1
        """ Thickness of pen"""
        self.progress_percentage: float = progress
        """ Progress of the hangman drawing"""
        self.max_attempts: int = max_attempts
        """ Max attempts of the hangman"""
        self.attempts: int = self.max_attempts
        """ Remaining attempts"""
        self.debug_anim: bool = debug_anim
        """ Debug flag"""
        self.reply_handler = reply_handler
        """ Reply callback function for the reply button click"""
        self.home_handler = home_handler
        """ Home callback function for the home button click"""
        self.score_feed: list[Score] = []
        """ List of the score feed show in the left of the hangman view"""

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
        """ Animation progress integer used to keep track of the progress of the damage animation"""
        self.damageTimer: QTimer = QTimer()
        """ Damage animation timer used to create the damage animation"""
        self.overlay: float = 1
        """ Animation progress integer used to keep track of the progress of the overlay animation"""
        self.overlayTimer: QTimer = QTimer()
        """ Overlay animation timer used to create the overlay animation"""

        self.effect: QSoundEffect = None
        """ Sound effect played for the wrong guesses"""
        self.home_button: Button = None
        """ Home button """
        self.reply_button: Button = None
        """ Reply button """

        self.scoreView: ScoreView = None
        """ Score view that contains the feed of scores"""

        self.damageTimer.timeout.connect(lambda: self.damageAnim())
        self.overlayTimer.timeout.connect(lambda: self.overlayAnim())

    def setScoreView(self, scoreView: ScoreView) -> None:
        """
            Setter for the Score View

            Parameters:
            scoreView (ScoreView): New scoreView

            Returns:
            None

        """
        self.scoreView = scoreView

    def showReplayButton(self, duration: int = 5) -> None:
        """
            Show reply button

            Parameters:
            duration (int): Duration of animation

            Returns:
            None

        """
        self.overlayTimer.start(duration)

    def hideReplayButton(self) -> None:
        """
            Hide reply button

            Returns:
            None

        """
        self.overlayTimer.stop()
        self.setOverlay(1)

    def startDamageAnimation(self, duration: int = 5) -> None:
        """
            Start damage animation

            Parameters:
            duration (int): Duration of animation

            Returns:
            None

        """
        self.damageAnimValue = 1
        self.damageTimer.start(duration)

    def takeDamage(self) -> None:
        """
            Take damage by progressing the hangman stage with sound and animation feedback

            Returns:
            None

        """
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

    def setReplayHandler(self, handler, append: bool = True) -> None:
        """
            Update replay button handler

            Parameters:
            handler (callable): New handler
            append (bool): True if appending the new handler to the existing handler

            Returns:
            None

        """
        func = self.reply_handler
        if self.reply_handler is not None and append:
            self.reply_handler = lambda: [func(), handler()]
        else:
            self.reply_handler = lambda: handler()

    def setHomeHandler(self, handler, append: bool = True) -> None:
        """
            Update home button handler

            Parameters:
            handler (callable): New handler
            append (bool): True if appending the new handler to the existing handler

            Returns:
            None

        """
        func = self.home_handler
        if self.home_handler is not None and append:
            self.home_handler = lambda: [func(), handler()]
        else:
            self.home_handler = lambda: handler()

    def setStageProgress(self, progress_percentage: float) -> None:
        """
            set progress_percentage to the new value

            Parameters:
            progress_percentage (int): New progress_percentage value

            Returns:
            None

        """
        self.progress_percentage = progress_percentage

    def setMaxAttempts(self, max_attempts: int) -> None:
        """
            Setter for the max_attempts

            Parameters:
            max_attempts (str): New max_attempts

            Returns:
            None

        """
        self.max_attempts = max_attempts
        self.attempts = max_attempts

    def reset(self) -> None:
        """
            Resets the hangman view

            Returns:
            None

        """
        self.attempts = self.max_attempts
        self.setOverlay(0)
        self.damageAnimValue = 0
        self.setStageProgress(0)
        self.repaint()
        self.damageTimer.stop()
        self.overlayTimer.stop()
        # self.showReplayButton(5)

    def setOverlay(self, overlay: float) -> None:
        """
            Setter for the overlay

            Parameters:
            overlay (float): New overlay value

            Returns:
            None

        """
        if 0 < overlay < 1:
            self.overlay = overlay
        elif overlay < 0:
            self.overlay = 0
        else:
            self.overlay = 1

        self.home_button.setOpacity(int(255 * ((1 - self.overlay) * 2)))
        self.reply_button.setOpacity(int(255 * ((1 - self.overlay) * 2)))

    def overlayAnim(self) -> None:
        """
            Overlay animation callback

            Returns:
            None

        """
        if self.overlay < 0.5:
            self.overlayTimer.stop()
        else:
            self.setOverlay(self.overlay - 0.01)
            self.repaint()

    def damageAnim(self) -> None:
        """
            Overlay animation callback

            Returns:
            None

        """
        if self.damageAnimValue <= 0:
            self.damageAnimValue = 1
        self.damageAnimValue -= 0.05
        if self.damageAnimValue < 0:
            self.damageTimer.stop()
        else:
            self.repaint()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        regionRect: QRectF = self.getHangmanRect()
        rect = regionRect.toRect()
        self.home_button = Button(rect.left(), rect.top() + int(0.7 * rect.height()), rect.width(), rect.height(), 0.8,
                                  0.2,
                                  bg_color=QColor(66, 205, 82))

        self.reply_button = Button(rect.left(), rect.top() + int(0.3 * rect.height()), rect.width(), rect.height(), 0.8,
                                   0.2,
                                   bg_color=QColor(66, 205, 82))
        self.setOverlay(self.overlay)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.debug_anim:
            self.takeDamage()
            self.attempts = self.max_attempts
            self.progress_percentage = 1

        # Reply
        self.reply_button.eventHandle(event, self.reply_handler)

        # Home button
        self.home_button.eventHandle(event, self.home_handler)

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

        if self.reply_button.isActive():
            self.drawReplayButton(qp, self.reply_button)
        if self.home_button.isActive():
            self.drawHomeButton(qp, self.home_button)

        qp.end()

    def getHangmanRect(self) -> QRectF:
        """
            Getter for the hangman box rectangle.

            Returns:
            QRectF: Area of the hangman drawing will take

        """
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
        """
            Getter for the hangman box rectangle.

            Parameters:
            hangmanRect (QRectF): Area of hangman box rectangle.

            Returns:
            QRectF: Area of the score feed rectangle will take

        """
        width: int = self.width()
        leftSpacingWidth = int((width - hangmanRect.width()) / 2)

        return QRectF(self.width() // 2 + int(hangmanRect.width() / 2), 0, leftSpacingWidth, self.height())

    def drawScoreFeed(self, painter: QPainter, hangmanRect: QRectF) -> None:
        """
            Draw Score feed

            Parameters:
            painter (QPainter): Painter of the paintEvent
            hangmanRect (QRectF): Area of hangman box rectangle.

            Returns:
            None

        """
        painter.setBrush(QColor(255, 27, 24))
        socreFeedRect = self.getScoreFeedRect(hangmanRect)

        score_feed = self.scoreView.getFeed()
        for i in range(0, len(score_feed)):
            score = score_feed[i]
            button = Button(socreFeedRect.left(),
                            socreFeedRect.top() + (i + 1) * socreFeedRect.height() * 0.12,
                            socreFeedRect.width(),
                            socreFeedRect.height(), 0.5, 0.1,
                            text=str(score), fg_color=QColor(255, 255, 255, 255),
                            bg_color=score.getBGColor(255),
                            border_color=score.getPen(255).color()
                            )
            button.setOpacity(int(255 * (5 - i) / 5))
            button.drawButton(painter)

    def drawHomeButton(self, painter: QPainter, button: Button) -> None:
        """
            Draw home button

            Parameters:
            painter (QPainter): Painter of the paintEvent
            hangmanRect (QRectF): Area of hangman box rectangle.

            Returns:
            None

        """

        center = button.rect.center()

        length = button.getLength()
        button.drawButton(painter)

        color_icon = QColor(255, 255, 255, int(255 * ((1 - self.overlay) * 2)))
        pen = QPen(color_icon)

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

    def drawReplayButton(self, painter: QPainter, button: Button) -> None:
        """
            Draw replay button

            Parameters:
            painter (QPainter): Painter of the paintEvent
            hangmanRect (QRectF): Area of hangman box rectangle.

            Returns:
            None

        """
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        # painter.setPen(pen)

        center = button.rect.center()

        length = button.getLength()
        button.drawButton(painter)

        color_icon = QColor(255, 255, 255, int(255 * ((1 - self.overlay) * 2)))
        startAngle = 0 * 16
        spanAngle = -270 * 16
        pen = QPen(color_icon)
        pen.setWidth(int(button.getHeight() / 10))
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
        """
            Draw base of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
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
        """
            Draw poll of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
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
        """
            Draw top bar of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
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
        """
            Draw support bar of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        painter.setBrush(color)
        painter.drawPolygon(
            QtGui.QPolygon([
                QPoint(left + int(width * 0.4), top + int(height * 0.2)),
                QPoint(left + int(width * 0.4) + self.thickness, top + int(height * 0.2)),
                QPoint(left + int(width * 0.2), top + int(height * 0.4) + self.thickness),
                QPoint(left + int(width * 0.2), top + int(height * 0.4))
            ]))

    def drawHanger(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw hanger of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        pen.setWidth(self.thickness // 2)
        painter.setPen(pen)

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.2))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        painter.drawLine(start, end)

    def drawHead(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw head of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))
        painter.setBrush(color)

        radius = int(self.thickness * 1.5)
        center = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))

        painter.drawEllipse(center, radius, radius)

    def drawBody(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw body of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.35))
        end = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        painter.drawLine(start, end)

    def drawLeftArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw left arm of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawRightArm(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw right arm of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.4))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.5))
        painter.drawLine(start, end)

    def drawLeftLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw left leg of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.5) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def drawRightLeg(self, painter: QPainter, color: QColor, left: int, top: int, width: int, height: int) -> None:
        """
            Draw right leg of hangman

            Parameters:
            painter (QPainter): Painter of the paintEvent
            color (QColor): Color of the drawing
            left (int): left corner of the drawing box
            top (int): top corner of the drawing box
            width (int):width of the available space
            height (int): height of the available space

            Returns:
            None

        """
        pen = QPen(color)
        painter.setPen(self.initPen(pen))

        start = QPoint(left + int(width * 0.6) + self.thickness, top + int(height * 0.6))
        end = QPoint(left + int(width * 0.7) + self.thickness, top + int(height * 0.7))
        painter.drawLine(start, end)

    def initPen(self, pen: QPen) -> QPen:
        """
            Show character at an index

            Parameters:
            index (int): Index of character in a word that you want to show

            Returns:
            None

        """
        pen.setWidth(self.thickness // 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        return pen


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
