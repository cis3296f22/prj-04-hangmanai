import sys

from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets, uic


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.form_widget = LifeCircle()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class LifeCircle(QtWidgets.QWidget):
    """
        Simple Button Class for the Hangman game UI.

        This can add the flexible button to the hangman UI with text, button function, custom colors (background, foreground, border)

    """
    def __init__(self, assets_dir: str = "../assets"):
        super(LifeCircle, self).__init__()
        uic.loadUi(assets_dir + '/ui/lifeCircle_v2.ui', self)
        # self.setContentsMargins(2, 2, 2, 2)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.circleFrame,
                                                     blurRadius=9.0,
                                                     color=QtGui.QColor(130, 130, 130),
                                                     offset=QtCore.QPointF(2.0, 2.0)
                                                     )
        self.setGraphicsEffect(shadow)

    def setEnabled(self, boolean: bool) -> None:
        self.circleFrame.setEnabled(boolean)

    def isEnabled(self) -> bool:
        return self.circleFrame.isEnabled()

    def reset(self) -> None:
        """
            Resets the LifeCircle by showing the circle to user

            Returns:
            None

        """
        self.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
