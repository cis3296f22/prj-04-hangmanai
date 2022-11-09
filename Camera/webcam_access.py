import cv2
from matplotlib import pyplot as plt


# takes a picture from the webcam with the id == 0
def take_pic(frame):
    saved = False
    cv2.imwrite('capture_frame.jpg', frame)


# finds the preferred camera the user wants
# figure it out later
def determine_camera():
    cam_id = 0
    return cam_id


# starts webcam capture video
def start_capture(cam_id):
    capture = cv2.VideoCapture(cam_id)
    cv2.namedWindow("Hangman Webcam")

    # until webcam is closed have live feed
    while capture.isOpened():
        ret, frame = capture.read()
        # shows active webcam feed
        cv2.imshow("Hangman Webcam", frame)

        # window waits for key press and record value
        waitResult = cv2.waitKey(1)

        # check ascii table
        if waitResult == 27:  # if the escape key was pressed it will exit
            break
        elif waitResult == 32:  # if the space key was pressed it will capture image
            take_pic(frame)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_capture(0)
# captures a frame from the camera with the id == 0
# should loop to see which camera the user wants to use?
# capture = cv2.VideoCapture(0)

# ret is a boolean if a frame was captured
# frame data from the webcam
# ret, frame = capture.read()
