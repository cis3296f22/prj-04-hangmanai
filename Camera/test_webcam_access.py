import cv2
import pytest

from Camera.webcam_access import Webcam_Access


def test_determine_camera():
    webcam = Webcam_Access()
    cam_found = webcam.determine_camera()
    if cam_found > -1:
        assert True
    else:
        assert False


def test_take_pic():
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
    with pytest.raises(Exception) as ex:
        webcam = Webcam_Access()
        webcam.start_capture(0)
    assert True
