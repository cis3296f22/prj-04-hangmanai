import time
import sys
from subprocess import call
import cv2

cam = cv2.VideoCapture()

while True:
    cam.open(0)
    image = cam.read()
    cv2.imwrite("current.jpeg",image[1])
    print("aaaa")
    time.sleep(10)
    break
