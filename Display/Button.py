from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QMouseEvent


class Button:
    """
        Simple Button Class for the Hangman game UI.

        This can add the flexible button to the hangman UI with text, button function, custom colors (background, foreground, border)

        Parameters:
        arg1 (int): Description of arg1

        Returns:
        int: Description of return value

        """
    def __init__(self, left: int, top: int, width: int, height: int,
                 width_ratio: float, height_ratio: float, text: str = "",
                 fg_color: QColor = QColor(0, 0, 0, 0), bg_color: QColor = QColor(0, 0, 0),
                 border_color: QColor = QColor(0, 0, 0, 0),
                 hide: bool = False
                 ):

        self.left: int = left
        """left potion of the button"""
        self.top: int = top
        """ top potion of the button"""
        self.width: int = width
        """ Whole width of the button box"""
        self.height: int = height
        """ Whole height of the button box"""
        self.width_ratio: float = width_ratio
        """ Content width ratio to the whole width of the button box"""
        self.height_ratio: float = height_ratio
        """ Content height ratio to the whole width of the button box"""
        self.rect: QRectF = self.getButtonRect()
        """ Rectangle box of the button """
        self.opacity: int = 255
        """ Opacity of the button out of 255"""
        self.text: str = text
        """ Text inside of the button"""
        self.fg_color: QColor = fg_color
        """ Text color of the button"""
        self.bg_color: QColor = bg_color
        """ Background color of the button"""
        self.border_color: QColor = border_color
        """ Border color of the button"""

        if hide:
            self.hide()

    def isActive(self) -> bool:
        """
            Check if the button is active or shown to the user.

            Returns:
            bool: True if button is visible to the user, False if not

        """
        return not self.opacity == 0

    def setOpacity(self, opacity: int) -> None:
        """
            Sets the opacity of the button

            Parameters:
            opacity (int): Opacity in int between 0 and 255

            Returns:
            None

        """
        if opacity < 0 or opacity > 255:
            print("Opacity should be between 0 and 255")
            return
        # print("Change opacity")
        self.opacity = opacity
        self.border_color.setAlpha(self.opacity)
        self.bg_color.setAlpha(self.opacity)
        self.fg_color.setAlpha(self.opacity)

    def hide(self) -> None:
        """
            Hides the button

            Returns:
            None

        """
        self.opacity = 0

    def eventHandle(self, event: QMouseEvent, handler=lambda: print("Default handler"),
                    pre_handler=lambda: print("prehandler")) -> None:
        """
            Executes the handler given depending on the condition of the given event

            Parameters:
            event (QMouseEvent): Invoked event from caller
            handler (callable): Invoked event from caller

            Returns:
            None

        """
        if handler is not None:
            pre_handler()
            if self.isActive() and self.rect.contains(event.position()):
                handler()

    def wordWidth(self, word: str, fontSize: float) -> float:
        """
            Calculate the width of the word given in the parameter with the specified font size

            Parameters:
            word (str): Word in string
            fontSize (int): Font size of the word

            Returns:
            float: Width of the word

        """
        slope = 0.7331 * fontSize - 0.0438
        intercept = -0.0729 * fontSize + 0.1588
        return len(word) * slope + intercept

    def fontSize(self, word: str, availableWidth: float, availableHeight: float, marginRatio: float = 1) -> int:
        """
            Calculate the font size of the word given in the parameter that can fill up the given dimension.

            Parameters:
            word (str): Word in string
            availableWidth (float): Available width for the word in float pixel
            availableHeight (float): Available height for the word in float pixel
            marginRatio (float): Margin ratio to the either width or height.

            Returns:
            int: Font size of the word

        """
        widthForHeight = self.wordWidth(word, availableHeight * marginRatio * 3 / 4)
        if widthForHeight > availableWidth * marginRatio:
            return int(self.fontSizeForWidth(word, availableWidth * marginRatio))
        return int(availableHeight * marginRatio * 3 / 4)

    def fontSizeForWidth(self, word: str, width: float) -> int:
        """
            Calculate the font size of the word given in the parameter that can fill up the given width of space.

            Parameters:
            word (str): Word in string
            width (float): Available width for the word in float pixel

            Returns:
            int: Font size of the word

        """
        return int((width + 0.0438 * len(word) - 0.1588) / (len(word) * 0.7331 - 0.1))  # 0.0729

    def getButtonRect(self) -> QRectF:
        """
            Create the bounding rectangle for the button box

            Returns:
            QRectF: Rectangle of the dimension occupied by the button

        """
        center = QPointF(self.left + 0.5 * self.width, self.top)
        size = QPointF(self.width * self.width_ratio, self.height * self.height_ratio)
        return QRectF(
            (center - size / 2),
            (center + size / 2)
        )

    def getTop(self) -> float:
        """
            Getter for the top field

            Returns:
            float: top class variable

        """
        return self.rect.top()

    def getLeft(self) -> float:
        """
            Getter for the left field

            Returns:
            float: left class variable

        """
        return self.rect.left()

    def getWidth(self) -> float:
        """
            Getter for the width field

            Returns:
            float: width class variable

        """
        return self.rect.width()

    def getHeight(self) -> float:
        """
            Getter for the height field

            Returns:
            float: height class variable

        """
        return self.rect.height()

    def getLength(self) -> float:
        """
            Returns the longer length of either width or height

            Returns:
            float: the longer length of either width or height

        """
        return self.rect.height() if self.rect.height() < self.rect.width() else self.rect.width()

    def drawButton(self, painter: QPainter) -> None:
        """
            Draws the button using the given painter.

            Parameters:
            painter (QPainter): painter from the parent paintEvent

            Returns:
            None

        """
        length = self.getLength()
        corner_radius = int(length) / 2
        painter.setPen(self.border_color)
        painter.setBrush(self.bg_color)

        painter.drawRoundedRect(self.rect, corner_radius, corner_radius)

        painter.setFont(QFont("Consolas", self.fontSize(str(self.text), self.rect.width(), self.rect.height(), 0.65)))
        painter.setPen(QPen(self.fg_color))
        painter.drawText(self.rect, Qt.AlignmentFlag.AlignCenter, str(self.text))
