import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import cv2
import pytesseract
from numpy import array

import threading


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
    """
        CameraThread will keep update the camera feed in the MainFrame and gives the life camera feedback to the user.

    """
    ImageUpdate = pyqtSignal(QImage)
    """ Image update signal"""

    def __init__(self, container: QLabel, recognition_callback=lambda x: print(x), parent=None):
        super().__init__(parent)
        self.container = container
        """ Container QLabel of the camera image"""
        self.width: int = 320
        """ Width of the camera image"""
        self.height: int = 240
        """ Height of the camera image"""
        self.cameraNo = 0
        """ Camera number used for the image capture"""
        self.recognition_callback = recognition_callback
        """ Callback function for the successful image recognition"""
        self.stack = []
        """ Stack for stack analyzer"""

        self.ImageUpdate.connect(self.ImageUpdateSlot)

    def ImageUpdateSlot(self, image: QImage) -> None:
        """
            Callback function used to update the camera image in the container to the new image

            Parameters:
            image (QImage): New image to the camera view

            Returns:
            float: Width of the word

        """
        self.container.setPixmap(QPixmap.fromImage(image))

    def changeCamera(self, no: int) -> None:
        """
            Change the camera to the new camera with the specified camera number

            Parameters:
            no (int): New camera number

            Returns:
            None

        """
        self.sleep(2)
        self.cameraNo = no
        self.Capture = cv2.VideoCapture(self.cameraNo)

    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(self.cameraNo)
        count = 0
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        analyzing_thread1 = TesseractThread(lambda: print("analyzing thread ready"))
        analyzing_thread2 = TesseractThread(lambda: print("analyzing thread ready"))
        lock = threading.Lock()

        while self.ThreadActive:
            ret, frame = self.Capture.read()
            ## Modify from here

            if ret:

                if not analyzing_thread1.isRunning():
                    analyzing_thread1 = TesseractThread(lambda: self.analyze(frame, lock))
                    analyzing_thread1.start()
                elif not analyzing_thread2.isRunning():
                    # a = 1
                    analyzing_thread2 = TesseractThread(lambda: self.analyze(frame, lock))
                    analyzing_thread2.start()

                # Keep of bit modify
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(Image, 1)
                # ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format.Format_RGB888)

                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        print("Finished")

    def analyze(self, frame, lock) -> None:
        """
            Analysing the image in the frame and extract the text from the image and append it to the stack.

            If the stack is full, call the callback function to notify the text recognition to the game

            Parameters:
            frame : Frame of Open CV
            lock : Lock used in multithreading

            Returns:
            None

        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        msk = cv2.inRange(hsv, array([0, 0, 0]), array([179, 255, 80]))
        krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
        dlt = cv2.dilate(msk, krn, iterations=1)
        thr = 255 - cv2.bitwise_and(dlt, msk)

        string = pytesseract.image_to_string(thr, lang='eng',
                                             config=' --psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # checks if the pytesseract passes a ''
        lock.acquire()
        if (len(string) > 0):
            # if string is not empty takes the first letter and adds to stack
            self.stack.append(string[:1])

        # if stack is length 10 checks most common letter
        if (len(self.stack) > 10):
            counter = 0
            cha = self.stack[0]

            for i in self.stack:
                curr_frequency = self.stack.count(i)
                if (curr_frequency > counter):
                    counter = curr_frequency
                    cha = i
            # prints out the most common letter
            print("the character " + cha)
            print(self.stack)
            self.recognition_callback(cha)
            self.stack.clear()
        lock.release()


class TesseractThread(QThread):
    def __init__(self, handler: lambda: print("Handler"), parent=None):
        super().__init__(parent)
        self.handler = handler
        """ Function to execute when in run()"""

    def run(self):
        self.handler()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
