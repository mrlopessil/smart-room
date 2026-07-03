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

def encode_image(path):
    img = Image.open(path)
    img.thumbnail((320,240))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=40, optimize=True)

    return b64encode(buffer.getvalue()).decode("utf-8")

last_presence_publish = 0
last_alarm_publish = 0
last_seen_publish = 0

detector = DetectPerson()
face = FaceRecognizer()

video_capture = cv2.VideoCapture(CAMERA)

box_annotator = sv.BoxAnnotator()

last_faces = set()

frame_count = 0
while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    frame_count += 1

    people = None
    if frame_count % 3 == 0:
        people = detector.detect(frame)

    if people is None:
        cv2.imshow("Camera", frame)
        if cv2.waitKey(30) == 27:
            break
        continue

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

        if frame_count % 10 == 0:
            print(recognized_names)
            
        known_faces = [n for n in recognized_names if n != "unknown"]
        current_faces = set(known_faces)
        
        only_unknown = len(known_faces) == 0
        faces_changed = current_faces != last_faces

        if time.time() - last_seen_publish > NO_PERSON_DETECTED_TIMEOUT and (faces_changed or only_unknown):
            filename = "snapshots/last_seen.jpg"
            cv2.imwrite(filename, frame)
            cleanup_snapshots()

            last_seen_stream = encode_image(filename)
            last_seen(last_seen_stream)

            last_seen_publish = time.time()

            last_faces = current_faces.copy()

        if time.time() - last_alarm_publish > NO_PERSON_DETECTED_TIMEOUT:
            intruder = len(known_faces) == 0 and len(recognized_names) > 0

            if intruder:
                print("Intruso detectado - ativando alarme")
                alarm_on()
                filename = f"snapshots/intruder{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                cleanup_snapshots()

                last_invader_stream = encode_image(filename)
                invader(last_invader_stream)
            else:
                print(f"Rosto reconhecido: {recognized_names}")
                alarm_off()

            last_alarm_publish = time.time()
            
    else:
        if time.time() - last_presence_publish > NO_PERSON_DETECTED_TIMEOUT:
            ac_off()
            light_off()

            last_presence_publish = time.time()


    cv2.imshow("Camera", frame)

    if cv2.waitKey(30) == 27:
        break

video_capture.release()
cv2.destroyAllWindows()