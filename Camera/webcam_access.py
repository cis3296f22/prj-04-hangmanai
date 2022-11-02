import cv2
from matplotlib import pyplot as plt


# takes a picture from the webcam with the id == 0
def take_pic():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    cv2.imwrite('picture.png', frame)
    capture.release()


# finds the preferred camera the user wants
# figure it out later
def determine_camera():
    cam_id = 0
    return cam_id


# starts webcam capture video
def start_capture(cam_id):
    capture = cv2.VideoCapture(cam_id)

    # until webcam is closed have live feed
    while capture.isOpened():
        ret, frame = capture.read()

        # shows active webcam feed
        cv2.imshow('Hangman text', frame)

        # window waits for key press and if it is q it will close
        # can use this for taking picture?
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


start_capture(0)
# captures a frame from the camera with the id == 0
# should loop to see which camera the user wants to use?
# capture = cv2.VideoCapture(0)

# ret is a boolean if a frame was captured
# frame data from the webcam
# ret, frame = capture.read()
