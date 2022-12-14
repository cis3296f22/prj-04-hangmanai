import sys

from PyQt6 import QtWidgets, uic, QtCore

from Display.LifeCircle import LifeCircle


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.form_widget = LifeBox()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.form_widget.takeLife(self.form_widget.reset))
        self.timer.start(1000)
        print(type(lambda: self.form_widget.takeLife(self.form_widget.reset)))


class LifeBox(QtWidgets.QWidget):
    """
        View that shows the remaining life for the hangman game with circles

    """

    def __init__(self, max_attempts: int = 5, assets_dir: str = "../assets"):
        super(LifeBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/lifeBox.ui', self)
        self.assets_dir: str = assets_dir
        """ Path to asset directory"""
        self.max_attempts: int = max_attempts
        """ Max attempts or maximum life circle can be displayed in the LifeBox"""
        self.life: int = max_attempts
        """ Remaining life"""
        self.lifeCircleList: list[LifeCircle] = []
        """ List of the LifeCircle in LifeBox"""

        self.lifeFrame.setLayout(QtWidgets.QHBoxLayout())
        self.setLife(self.max_attempts)

    def setLife(self, number: int) -> None:
        """
            Sets the life in the LifeBox

            Parameters:
            number (int): New life in int

            Returns:
            None

        """
        self.life = number
        if self.life > self.max_attempts:
            print("You cannot assign more life than max life specified -> " + str(self.life))
            return

        if self.life < 0:
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

    def getLife(self) -> int:
        """
            Getter for the life in the LifeBox

            Returns:
            int: current life

        """
        return self.life

    def isZero(self) -> bool:
        """
            Checks if the life is zero

            Returns:
            bool: True if life is zero

        """
        if self.life <= 0:
            return True
        else:
            return False

    def setMaxAttempts(self, max_attempts: int) -> None:
        """
            Setter for the max_attempts

            Parameters:
            max_attempts (str): New max_attempts

            Returns:
            None

        """
        self.max_attempts = max_attempts
        self.setLife(self.max_attempts)

    def takeLife(self, zeroHandler: callable(any)) -> None:
        """
            Decrement life by one and executes the zeroHandler when life is zero

            Parameters:
            zeroHandler (callable): Callback function that will be called when life is zero

            Returns:
            None

        """
        self.life = self.life - 1
        self.setLife(self.life)
        if self.isZero():
            zeroHandler()

    def reset(self) -> None:
        """
            Resets the LifeBox by showing the all of life

            Returns:
            None

        """
        self.setLife(self.max_attempts)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
