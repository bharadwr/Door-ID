import cv2
import sys
from uuid import uuid4
from time import time

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

def find_face_from_webcam():
    imageName = ""
    startTime = time()

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(1)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            imageName = "{}.jpg".format(str(uuid4()))
            cv2.imwrite(imageName, frame)
            break

        if time() - startTime > 10:
            break

        # Display the resulting frame
        # cv2.imshow('FaceDetection', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

    return imageName

if __name__ == "__main__":
    print(find_face_from_webcam())
