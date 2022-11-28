import sys

from PyQt6 import QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import (QPoint, QRect,
                          QTimer, QUrl)
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygon, QFont
from PyQt6.QtMultimedia import QSoundEffect

from Camera.webcam_access import Webcam_Access
from Display.Button import Button
from Display.CameraThread import CameraThread
from Display.ScoreView import ScoreView
from Score import Score

SOUND_FILE = "sound/knife.wav"


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = CameraSwitchView(None)
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class CameraSwitchView(QtWidgets.QWidget):
    def __init__(self, camera_thread: CameraThread, assets_dir: str = "../assets"):
        super(CameraSwitchView, self).__init__()

        self.assets_dir: str = assets_dir
        self.camera_thread = camera_thread
        self.selected_index = 0
        self.buttons = []

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        width = self.width()
        height = self.height()
        web_cams = Webcam_Access().print_camera_list()

        self.buttons.clear()
        for i in range(len(web_cams)):
            self.buttons.append(Button(0, int(height / 1 / len(web_cams) * (1 / 2 + i)), width, height, 0.8, 1 / len(web_cams) / 1.5,
                        text=web_cams[i], bg_color=QColor(66, 205, 82), fg_color=QColor(255, 255, 255)))

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.camera_thread is not None:
            for i in range(len(self.buttons)):
                self.buttons[i].eventHandle(event,
                                            handler= lambda: [self.camera_thread.changeCamera(i), self.changeSelection(i)])
        else:
            for i in range(len(self.buttons)):
                self.buttons[i].eventHandle(event, lambda: print("Non thread handler"))
        self.repaint()

    def changeSelection(self, index: int) -> None:
        self.selected_index = index

    def paintEvent(self, e) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setBrush(QColor(255, 0, 0))

        for i in range(len(self.buttons)):
            if i == self.selected_index:
                self.buttons[i].setOpacity(255)
            else:
                self.buttons[i].setOpacity(75)
            self.buttons[i].drawButton(qp)

        qp.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
