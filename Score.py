import PyQt6.QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen


class Score:
    def __init__(self, value: int = 0, name: str = "NONE", bgColor: QColor = QColor(0, 0, 0), pen: QPen = QPen(QColor(255, 255, 255))):
        self.bgColor = bgColor
        self.value = value
        self.name = name
        self.pen = pen

    def __str__(self):
        return self.name + " +" + str(self.value)

    def getPen(self, alpha: int = 255):
        color = self.pen.color()
        color.setAlpha(alpha)
        pen = QPen(self.pen)
        pen.setColor(color)
        return pen

    def getBGColor(self, alpha: int = 255):
        color = self.bgColor
        color.setAlpha(alpha)
        return color

    @staticmethod
    def CORRECT(duplicate=1):
        return Score(5 * duplicate, "CORRECT", QColor(66, 205, 82), QPen(Qt.PenStyle.NoPen))

    @staticmethod
    def WRONG():
        return Score(0, "WRONG", QColor(44, 44, 44), QPen(QColor(66, 205, 82), 1))

    @staticmethod
    def WIN():
        return Score(20, "WIN", QColor(89,187,241), QPen(Qt.PenStyle.NoPen))

    @staticmethod
    def LOSE():
        return Score(0, "LOSE", QColor(216,12,18), QPen(QColor(25, 25, 25), 1))


if __name__ == "__main__":
    print(Score.CORRECT().value)
    a = ["1234", "12345", "123456", "1234567"]
    b = filter(lambda x: len(x) < 5, a)
    print(list(b))
