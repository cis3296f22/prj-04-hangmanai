import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import cv2
import pytesseract
from numpy import array

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
        self.Worker1.cameraNo = self.Worker1.cameraNo + 1
        self.Worker1.changeCamera(self.Worker1.cameraNo)


class CameraThread(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, container: QLabel, parent=None):
        super().__init__(parent)
        self.container = container
        self.ImageUpdate.connect(self.ImageUpdateSlot)
        self.width = 320
        self.height = 240
        self.cameraNo = 0

    def updateContainer(self, container: QLabel):
        self.container = container

    def ImageUpdateSlot(self, Image):
        self.container.setPixmap(QPixmap.fromImage(Image))

    def changeCamera(self, no):
        self.sleep(2)
        self.cameraNo = no
        self.Capture = cv2.VideoCapture(self.cameraNo)


    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(self.cameraNo)
        count = 0
        stack = []
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        while self.ThreadActive:
            ret, frame = self.Capture.read()
            ## Modify from here

            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                msk = cv2.inRange(hsv, array([0, 0, 0]), array([179, 255, 80]))
                krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
                dlt = cv2.dilate(msk, krn, iterations=1)
                thr = 255 - cv2.bitwise_and(dlt, msk)

                string = pytesseract.image_to_string(thr, lang='eng',
                                                     config=' --psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

                # checks if the pytesseract passes a ''
                if (len(string) > 0):
                    # if string is not empty takes the first letter and adds to stack
                    stack.append(string[:1])

                # if stack is length 10 checks most common letter
                if (len(stack) > 10):
                    counter = 0
                    cha = stack[0]

                    for i in stack:
                        curr_frequency = stack.count(i)
                        if (curr_frequency > counter):
                            counter = curr_frequency
                            cha = i
                    # prints out the most common letter
                    print("the character " + cha)
                    stack.clear()

                # Keep of bit modify
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(Image, 1)
                # ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format.Format_RGB888)

                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        print("Finished")

    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())