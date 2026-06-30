import serial
from config import SERIAL_PORT, BAUD_RATE

class ESP32Controller:
    def __init__(self):
        self.serial = serial.Serial(SERIAL_PORT, BAUD_RATE)