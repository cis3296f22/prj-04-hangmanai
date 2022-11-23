import cv2
import pytesseract
from PIL import Image
import numpy as np


class Webcam_Access:

    cam_id = -1

    def __init__(self):
        self.cam_id = 0

    # takes a picture from the webcam with the id == 0
    def take_pic(self, frame):
        saved = cv2.imwrite('capture_frame.jpg', frame)
        return saved

    # finds the preferred camera the user wants
    # figure it out later
    def determine_camera(self):
        cam_id = self.cam_id
        # while(cam_id <= 10):
        #    cv2.namedWindow("Webcam #" + cam_id)
        #   cv2.createButton("Use this webcam",)

        #  cam_id += 1

        return cam_id

    # def set_camera(cam_id):

    # starts webcam capture video
    def start_capture(cam_id):
        # capture = cv2.VideoCapture(cam_id)
        cv2.namedWindow("Hangman Webcam")

        # https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
        myconfig = r"--psm 9 --oem 3"
        # psm: 8, 9!, 10
        # for executable install tesseract-ocr-data python package

        # pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        #
        cap = cv2.VideoCapture(0)
        count = 0
        while (True):

            ret, frame = cap.read()
        #
        #     # count += 1
        #     # if((count%10) == 0):
        #     hImg, wImg, _ = frame.shape
        #     x1, y1, w1, h1 = 0, 0, wImg, hImg
        #
        #     # make image grayscale
        #     img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        #     # preform dialation and erosion to remove excess noise
        #     kernel = np.ones((1, 1), np.uint8)
        #     img = cv2.dilate(img, kernel, iterations=20)
        #     img = cv2.erode(img, kernel, iterations=20)
        #
        #     # adds gaussian blur for easier processing
        #     img = cv2.adaptiveThreshold(img, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        #     # shows all effects applied
        #     cv2.imshow("img", img)
        #     boxes = pytesseract.image_to_boxes(img, config=myconfig)
        #     # print(boxes)
        #     string = pytesseract.image_to_string(img, config=myconfig)
        #     print(string)
        #     print(len(string))
        #     if len(string) <= 2:
        #         result = input("Is this your letter?(y/n) " + string)
        #         if result == 'y':
        #             exit(0)
        #
        #     for b in boxes.splitlines():
        #         b = b.split(' ')
        #         # print(b[0])
        #         x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        #         cv2.rectangle(frame, (x, hImg - y), (w, hImg - h), (0, 255, 0), 2)
        #
        #         #cv2.putText(frame,string,(x, hImg - y), (w, hImg - h),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        #
            cv2.imshow("Hangman Webcam", frame)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = Webcam_Access()
    cam.start_capture()
# captures a frame from the camera with the id == 0
# should loop to see which camera the user wants to use?
# capture = cv2.VideoCapture(0)
#
# ret is a boolean if a frame was captured
# frame data from the webcam
# ret, frame = capture.read()

