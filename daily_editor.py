import os
import datetime

# Where daily notes will live
DAILY_NOTES_DIR = "/storage/emulated/0/MutableMemory/daily_notes/"

def safe_read(path):
    """Return file contents or '(empty)' if unreadable."""
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "(empty)"

def open_in_nano(path):
    """Open a file in nano."""
    os.system(f"nano '{path}'")

def daily(mode=None):
    """
    View or edit today's daily note.
    Base call (daily) = CAT
    daily edit = open in nano
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(DAILY_NOTES_DIR, f"daily_{today}.txt")

    # Ensure folder exists
    os.makedirs(DAILY_NOTES_DIR, exist_ok=True)

    # Create file if missing
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"=== DAILY NOTE — {today} ===\n\n")

    # EDIT MODE
    if mode == "edit":
        open_in_nano(path)
        return

    # DEFAULT: CAT MODE
    print(safe_read(path))
