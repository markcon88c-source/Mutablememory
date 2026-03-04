import os
import datetime

DAILY_DIR = "/storage/emulated/0/MutableMemory/daily/"

def safe_read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "(empty)"

def open_in_nano(path):
    os.system(f"nano '{path}'")

def daily(mode=None):
    """CAT or edit today's daily note."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(DAILY_DIR, f"daily_{today}.txt")

    os.makedirs(DAILY_DIR, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"=== DAILY NOTE — {today} ===\n\n")

    if mode == "edit":
        open_in_nano(path)
        return

    print(safe_read(path))
