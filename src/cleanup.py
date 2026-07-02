import os
import time
from config import SNAPSHOTS_DIR, MAX_SNAPSHOTS_FILES

def cleanup_snapshots():
    files = [
        os.path.join(SNAPSHOTS_DIR, f)
        for f in os.listdir(SNAPSHOTS_DIR)
        if os.path.isfile(os.path.join(SNAPSHOTS_DIR, f))
    ]

    files.sort(key=os.path.getmtime)

    while len(files) > MAX_SNAPSHOTS_FILES:
        oldest = files.pop(0)

        try:
            os.remove(oldest)
            print(f"{time.time()} removido:", oldest)
        except Exception as e:
            print("erro ao remover:", e)