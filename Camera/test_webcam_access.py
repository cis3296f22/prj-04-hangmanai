import cv2
import pytest

from Camera.webcam_access import Webcam_Access

def test_print_camera_list():
    """Test to check if a list of devices is returned"""
    webcam = Webcam_Access()
    cam_list = webcam.print_camera_list()
    if len(cam_list) > 0:
        assert True
    else:
        assert False


def test_take_pic():
    """Test if it can capture a single frame from the webcam"""
    webcam = Webcam_Access()
    cam_id = webcam.determine_camera()
    print(cam_id)
    cap = cv2.VideoCapture(cam_id)
    ret, frame = cap.read()
    if ret == False:
        assert False
    result = Webcam_Access.take_pic(frame)
    if result == True:
        assert True



def test_start_capture():
    """Tests if the webcam starts to capture"""
    with pytest.raises(Exception) as ex:
        webcam = Webcam_Access()
        webcam.start_capture(0)
    assert True

