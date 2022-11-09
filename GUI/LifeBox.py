from PyQt6 import QtWidgets, uic
import sys
from GUI.LifeCircle import LifeCircle

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = LifeBox()
        self.setCentralWidget(self.form_widget)
        self.form_widget.setLife(self.form_widget.max_attempts - 1)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class LifeBox(QtWidgets.QWidget):
    def __init__(self, max_attempts=5, assets_dir="../assets"):
        super(LifeBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/lifeBox.ui', self)
        self.assets_dir = assets_dir
        self.max_attempts = max_attempts
        self.life = max_attempts
        self.lifeCircleList = []

        self.lifeFrame.setLayout(QtWidgets.QHBoxLayout())
        # self.lifeFrame.layout().setSpacing(15)
        self.setLife(self.max_attempts)

    def setLife(self, number):
        self.life = number
        if self.life > self.max_attempts:
            print("You cannot assign more life than max life specified -> " + str(self.life))
            return

        if self.life < 0 :
            print("You cannot assign less than 0. You are lost -> " + str(self.life))
            return

        for life_circle in self.lifeCircleList:
            self.lifeFrame.layout().removeWidget(life_circle)

        self.lifeCircleList.clear()

        for index in range(self.max_attempts):
            life_circle = LifeCircle(assets_dir=self.assets_dir)
            if index >= self.life:
                life_circle.setEnabled(False)
            self.lifeCircleList.append(life_circle)
            self.lifeFrame.layout().addWidget(life_circle)

    def setMaxAttempts(self, max_attempts):
        self.max_attempts = max_attempts
        self.setLife(self.max_attempts)

    def takeLife(self, zeroHandler):
        self.life = self.life - 1
        self.setLife(self.life)
        if self.life <= 0:
            zeroHandler()

    def blankAt(self, index):
        self.setCharacterAt(index, " ")

    def blank(self):
        self.setWord(" " * len(self.word))

    def reset(self):
        self.setWord("")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()