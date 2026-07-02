import python.src.face_recognition as face_recognition
import os
import numpy as np
import cv2
from python.config import FACES_PATH


class FaceRecognizer:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

        self.load_faces(FACES_PATH)

    def load_faces(self, path):

        for person in os.listdir(path):
            person_path = os.path.join(path, person)

            if not os.path.isdir(person_path):
                continue

            for img_name in os.listdir(person_path):

                if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                img_path = os.path.join(person_path, img_name)

                try:
                    image = face_recognition.load_image_file(img_path)

                    face_locations = face_recognition.face_locations(image)
                    encodings = face_recognition.face_encodings(image, face_locations)

                    for encoding in encodings:
                        self.known_encodings.append(encoding)
                        self.known_names.append(person)

                except Exception as e:
                    print(f"Erro em {img_path}: {e}")

        print(f"[INFO] Encodings carregados: {len(self.known_encodings)}")

    def recognize(self, face_image):

        if len(self.known_encodings) == 0:
            return "unknown"

        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(face_image)
        encodings = face_recognition.face_encodings(face_image, face_locations)

        if len(encodings) == 0:
            return "unknown"

        face_encoding = encodings[0]

        distances = face_recognition.face_distance(
            self.known_encodings,
            face_encoding
        )

        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]

        if best_distance < 0.6:
            return self.known_names[best_match_index]

        return "unknown"