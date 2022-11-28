from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QMouseEvent


class Button:
    def __init__(self, left: int, top: int, width: int, height: int,
                      width_ratio: float, height_ratio: float, text: str = "",
                      fg_color: QColor = QColor(0, 0, 0, 0), bg_color: QColor = QColor(0, 0, 0),
                      border_color: QColor = QColor(0, 0, 0, 0),
                        hide: bool = False
                 ):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.rect = self.getButtonRect()
        self.opacity = 255
        self.text = text
        self.fg_color: QColor = fg_color
        self.bg_color: QColor = bg_color
        self.border_color: QColor = border_color

        if hide:
            self.hide()

    def isActive(self) -> bool:
        return not self.opacity == 0

    def setOpacity(self, opacity: int):
        if opacity < 0 or opacity > 255:
            print("Opacity should be between 0 and 255")
            return
        print("Change opacity")
        self.opacity = opacity
        self.border_color.setAlpha(self.opacity)
        self.bg_color.setAlpha(self.opacity)
        self.fg_color.setAlpha(self.opacity)

    def hide(self):
        self.opacity = 0

    def eventHandle(self, event: QMouseEvent, handler=lambda: print("Default handler"),
                    pre_handler= lambda: print("prehandler")):
        if handler is not None:
            pre_handler()
            if self.isActive() and self.rect.contains(event.position()):
                handler()

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
        return int((width + 0.0438 * len(word) - 0.1588) / (len(word) * 0.7331 - 0.1)) # 0.0729

    def getButtonRect(self) -> QRectF:
        center = QPointF(self.left + 0.5 * self.width, self.top)
        size = QPointF(self.width * self.width_ratio, self.height * self.height_ratio)
        return QRectF(
            (center - size / 2),
            (center + size / 2)
        )

    def getTop(self) -> float:
        return self.rect.top()

    def getLeft(self) -> float:
        return self.rect.left()

    def getWidth(self) -> float:
        return self.rect.width()

    def getHeight(self) -> float:
        return self.rect.height()

    def getLength(self) -> float:
        return self.rect.height() if self.rect.height() < self.rect.width() else self.rect.width()

    def drawButton(self, painter: QPainter) -> None:

        length = self.getLength()
        corner_radius = int(length) / 2
        painter.setPen(self.border_color)
        painter.setBrush(self.bg_color)

        painter.drawRoundedRect(self.rect, corner_radius, corner_radius)

        painter.setFont(QFont("Consolas", self.fontSize(str(self.text), self.rect.width(), self.rect.height(), 0.65)))
        painter.setPen(QPen(self.fg_color))
        painter.drawText(self.rect, Qt.AlignmentFlag.AlignCenter, str(self.text))