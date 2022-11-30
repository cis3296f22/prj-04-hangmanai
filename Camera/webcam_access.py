import sys

import cv2
from numpy import array
import pytesseract
import numpy as np
from pygrabber.dshow_graph import FilterGraph


class Webcam_Access():

    cam_id = -1

    def __init__(self):
        self.cam_id = 0

    # takes a picture from the webcam with the id == 0
    def take_pic(frame):
        saved = cv2.imwrite('capture_frame.jpg', frame)
        return saved

    # finds the preferred camera the user wants
    # figure it out later
    def print_camera_list(self):


        graph = FilterGraph()

        print(graph.get_input_devices())  # list of camera device
        cam_list = graph.get_input_devices()

        #try:
         #   device = graph.get_input_devices().index("name camera that I want to use it ")

        #except ValueError as e:

         #   device = graph.get_input_devices().index("Integrated Webcam")

        return cam_list
    #return list of cameras

    # def set_camera(cam_id):

    # starts webcam capture video
    def start_capture(cam_id):
        #capture = cv2.VideoCapture(0)
        cv2.namedWindow("Hangman Webcam")

        # https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
        # myconfig = r"--psm 9 --oem 3"
        # psm: 8, 9!, 10
        # for executable install tesseract-ocr-data python package
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


        cap = cv2.VideoCapture(1)
        count = 0
        stack = []
        while (True):

            ret, frame = cap.read()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            msk = cv2.inRange(hsv, array([0, 0, 0]), array([179, 255 ,80]))
            krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
            dlt = cv2.dilate(msk, krn, iterations=1)
            thr = 255 - cv2.bitwise_and(dlt, msk)

            cv2.imshow("img", thr)

            #string = pytesseract.image_to_string(img)
            string = pytesseract.image_to_string(thr,lang='eng',config=' --psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            # checks if the pytesseract passes a ''
            if(len(string) > 0):
                # if string is not empty takes the first letter and adds to stack
                stack.append(string[:1])

            # if stack is length 10 checks most common letter
            if(len(stack) > 10):
                counter = 0
                cha = stack[0]

                for i in stack:
                    curr_frequency = stack.count(i)
                    if (curr_frequency > counter):
                        counter = curr_frequency
                        cha = i
                # prints out the most common letter
                print("the character " + cha)
                print(stack)
                stack.clear()
            if cv2.getWindowProperty("Hangman Webcam", cv2.WND_PROP_VISIBLE) < 1:
                break

            cv2.imshow("Hangman Webcam", frame)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
   Webcam_Access.start_capture(1)
# captures a frame from the camera with the id == 0
# should loop to see which camera the user wants to use?
# capture = cv2.VideoCapture(0)

# ret is a boolean if a frame was captured
# frame data from the webcam
# ret, frame = capture.read()