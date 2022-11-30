import cv2

from Camera.webcam_access import Webcam_Access
"""Simple script to run webcam_access.py"""
webcam = Webcam_Access()

Webcam_Access.start_capture(0)

print(webcam.print_camera_list())
