from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)
import sys
from GUI.LifeCircle import LifeCircle
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont
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
        qp.setPen(QtGui.QColor(168, 34, 3))
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

        print(left)
        print(top)
        print(width32)
        print(height32)
        rect = QtCore.QRect(left, top, width32, height32)

        qp.fillRect(rect, Qt.BrushStyle.SolidPattern)
        qp.end()


        painter = QtGui.QPainter(self)
        painter.begin(self)

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(0, 255, 255))
        # brush.setStyle(QtCore.Qt.SolidPattern)
        # print(painter.device().width())
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)





        rect1 = QtCore.QRect(top, left, width32, height32)
        brush1 = QtGui.QBrush()
        brush1.setColor(QtGui.QColor(0, 0, 0))
        painter.fillRect(rect1, brush1)






        painter.end()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()