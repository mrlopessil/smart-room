import face_recognition
import os
import numpy as np
from config import FACES_PATH

class FaceRecognizer:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

        self.load_faces(FACES_PATH)

    def load_faces(self, path):
        for person in os.path.join(path, person):
            person_path = os.path.join(path, person)

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)

            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                self.known_encodings.append(encodings[0])
                self.known_names.append(person)

    def recognize(self, face_image):
        encodings = face_recognition.face_encodings(face_image)

        if len(encodings) == 0:
            return "unknown"

        face_encoding = encodings[0]

        matches = face_recognition.compare_faces(self.known_encodings, face_encoding)

        if True in matches:
            index = matches.index(True)
            return self.known_names[index]
        
        return "unknown"

    