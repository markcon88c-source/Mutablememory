import os
import datetime

META_DIR = "/storage/emulated/0/MutableMemory/meta/"

def safe_read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "(empty)"

def open_in_nano(path):
    os.system(f"nano '{path}'")

def meta(mode=None):
    """View or edit today's meta note."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(META_DIR, f"meta_{today}.txt")

    os.makedirs(META_DIR, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"=== META NOTE — {today} ===\n\n")

    if mode == "edit":
        open_in_nano(path)
        return

    print(safe_read(path))
