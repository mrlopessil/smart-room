import cv2

from detector import DetectPerson
from config import CAMERA, NO_PERSON_DETECTED_TIMEOUT

detector = DetectPerson()

video_capture = cv2.VideoCapture(CAMERA)

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    people = detector.detect(frame)

    count = len(people)

    if count > 0:
        