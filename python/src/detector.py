from rfdetr import RFDETRNano
from python.config import PERSON_CLASS_ID

class DetectPerson:
	def __init__(self):
		self.model = RFDETRNano()

	def detect(self, frame):
		detections = self.model.predict(frame)

		people = detections[detections.class_id == PERSON_CLASS_ID]
			
		return people