import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.Worker1 = CameraThread(self.FeedLabel)

        self.Worker1.start()

        self.setLayout(self.VBL)



    def CancelFeed(self):
        self.Worker1.stop()

class CameraThread(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, container: QLabel, parent=None):
        super().__init__(parent)
        self.container = container
        self.ImageUpdate.connect(self.ImageUpdateSlot)
        self.width = 320
        self.height = 240

    def ImageUpdateSlot(self, Image):
        self.container.setPixmap(QPixmap.fromImage(Image))

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())