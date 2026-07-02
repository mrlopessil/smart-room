import cv2, time
from src.detector import DetectPerson
from src.adafruit_client import last_seen, invader, light_on, ac_on, light_off, ac_off, alarm_on, alarm_off
from src.face_recognition import FaceRecognizer
from config import CAMERA, NO_PERSON_DETECTED_TIMEOUT
import supervision as sv
from base64 import b64encode
from src.cleanup import cleanup_snapshots
from PIL import Image
import io

last_presence_publish = 0
last_alarm_publish = 0
last_seen_publish = 0

detector = DetectPerson()
face = FaceRecognizer()

video_capture = cv2.VideoCapture(CAMERA)

box_annotator = sv.BoxAnnotator()

last_faces = set()

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    people = detector.detect(frame)

    annotated_frame = box_annotator.annotate(
        scene=frame,
        detections=people
    )

    count = len(people)

    if count > 0:
        if time.time() - last_presence_publish > NO_PERSON_DETECTED_TIMEOUT:
            light_on()
            ac_on()

            last_presence_publish = time.time()

        recognized_names = []

        for box in people.xyxy:
            x1, y1, x2, y2 = map(int, box)
            person_crop = frame[y1:y2, x1:x2]

            name = face.recognize(person_crop)
            recognized_names.append(name)

        print(recognized_names)
        known_faces = [n for n in recognized_names if n != "unknown"]
        current_faces = set(known_faces)
        
        only_unknown = len(known_faces) == 0
        faces_changed = current_faces != last_faces

        if time.time() - last_seen_publish > NO_PERSON_DETECTED_TIMEOUT and (faces_changed or only_unknown):
            filename = "snapshots/last_seen.jpg"
            cv2.imwrite(filename, frame)
            cleanup_snapshots()

            img = Image.open(filename)
            img.thumbnail((320,240))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=40, optimize=True)

            stream = b64encode(buffer.getvalue()).decode("utf-8")

            last_seen(stream)

            last_seen_publish = time.time()
            last_faces = current_faces.copy()

        if time.time() - last_alarm_publish > NO_PERSON_DETECTED_TIMEOUT:
            intruder = len(known_faces) == 0

            if intruder:
                print("Intruso detectado - ativando alarme")
                alarm_on()
                filename = f"snapshots/intruder{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                cleanup_snapshots()

                invader(stream)
            else:
                print(f"Rosto reconhecido: {name}")
                alarm_off()

            last_alarm_publish = time.time()
            
    else:
        if time.time() - last_presence_publish > NO_PERSON_DETECTED_TIMEOUT:
            ac_off()
            light_off()

            last_presence_publish = time.time()


    cv2.imshow("Camera", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

video_capture.release()
cv2.destroyAllWindows()