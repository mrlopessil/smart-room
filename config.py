from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FACES_PATH = BASE_DIR / "data" / "faces"

# CAMERA
# Escolha da câmera a ser usada, 0 é a câmera default
CAMERA = 0

PERSON_CLASS_ID = 1
CONFIDENCE_THRESHOLD = 0.8

NO_PERSON_DETECTED_TIMEOUT = 10

# ADAFRUIT CONFIG
# Adcione o seu username do adafruit io e sua key
AIO_USERNAME = ""
AIO_KEY = ""

# FEEDS KEYS
# Mude o valor dos feeds para as keys do seus feeds
FEED_LIGHT = "light"
FEED_AC = "ac"
FEED_LAST_PERSON = "last-person"
FEED_INTRUDER = "invader-image"
FEED_ALARM = "alarm"

SNAPSHOTS_DIR = "snapshots"
MAX_SNAPSHOTS_FILES = 100