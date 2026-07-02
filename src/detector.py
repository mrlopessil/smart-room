from rfdetr import RFDETRNano
from config import PERSON_CLASS_ID
import torch

class DetectPerson:
	def __init__(self):
		self.model = RFDETRNano()
		self.model.optimize_for_inference(dtype=torch.float16)

	def detect(self, frame):
		detections = self.model.predict(frame)

		people = detections[detections.class_id == PERSON_CLASS_ID]
			
		return people