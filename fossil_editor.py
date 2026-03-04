import os
import datetime

FOSSIL_DIR = "/storage/emulated/0/MutableMemory/fossils/"

def safe_read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "(empty)"

def open_in_nano(path):
    os.system(f"nano '{path}'")

def fossil(mode=None):
    """View or edit today's fossil log."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(FOSSIL_DIR, f"fossil_{today}.txt")

    os.makedirs(FOSSIL_DIR, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"=== FOSSIL LOG — {today} ===\n\n")

    if mode == "edit":
        open_in_nano(path)
        return

    print(safe_read(path))
