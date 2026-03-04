import os
import sys
import json
import shutil
import datetime
from pathlib import Path

# ==============================
# REMEMGER — PATH SETUP
# ==============================
BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"
META_DIR = BASE_DIR / "meta"
COPILOT_NOTES_DIR = BASE_DIR / "copilot_notes"
ORGANS_DIR = BASE_DIR / "organs"
SNAPSHOTS_DIR = BASE_DIR / "snapshots"
ARCHIVE_DIR = BASE_DIR / "archive"

def open_in_nano(path):
    print("DEBUG: open_in_nano CALLED with:", path)
    os.system(f"nano '{path}'")

# Daily notes index file
DAILY_NOTES_INDEX = NOTES_DIR / "daily_notes_index.txt"

# Today’s note (auto‑generated daily file)
TODAY_NOTE_PATH = NOTES_DIR / f"daily_{datetime.date.today().isoformat()}.txt"

# Yesterday’s note
YESTERDAY_NOTE_PATH = NOTES_DIR / f"daily_{(datetime.date.today() - datetime.timedelta(days=1)).isoformat()}.txt"

for d in [NOTES_DIR, META_DIR, COPILOT_NOTES_DIR, ORGANS_DIR, SNAPSHOTS_DIR, ARCHIVE_DIR]:
    d.mkdir(exist_ok=True)

# ==============================
# JSON HELPERS  ← place here
# ==============================

def load_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default if default is not None else {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ==============================
# INDEX FILES  ← now this works
# ==============================

RESTORE_INDEX_PATH = META_DIR / "restore_index.json"
NOTES_INDEX_PATH = META_DIR / "notes_index.json"

restore_index = load_json(RESTORE_INDEX_PATH, default={"restores": []})
notes_index = load_json(NOTES_INDEX_PATH, default={"notes": []})
# ==============================
# DATE HELPERS
# ==============================

def today_str():
    return datetime.date.today().strftime("%Y-%m-%d")
def date_days_ago(n):
    target = datetime.date.today() - datetime.timedelta(days=n)
    return target.strftime("%Y-%m-%d")

def daily_note_path(date_str):
    return NOTES_DIR / f"daily_{date_str}.txt"

# ==============================
# FILE HELPERS
# ==============================

def safe_read(path):
    if not path.exists():
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def safe_write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def safe_append(path, content):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

# ==============================
# JSON HELPERS
# ==============================

def load_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default if default is not None else {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ==============================
# PRINT HELPERS
# ==============================

def header(title):
    print("\n" + "=" * 30)
    print(title)
    print("=" * 30 + "\n")

def list_files(directory):
    return sorted([p for p in directory.iterdir() if p.is_file()])

# ==============================
# FUZZY MATCHING (simple)
# ==============================

def fuzzy_match(query, options):
    """
    Returns best fuzzy match (case-insensitive).
    """
    q = query.lower()
    best = None
    best_score = -1

    for opt in options:
        o = opt.lower()
        score = 0
        for c in q:
            if c in o:
                score += 1
        if score > best_score:
            best_score = score
            best = opt

    return best
# ==============================
# ORGAN INDEX SYSTEM
# ==============================

ORGAN_INDEX_PATH = META_DIR / "organ_index.json"

def load_organ_index():
    index = load_json(ORGAN_INDEX_PATH, default={})
    return index

def save_organ_index(index):
    save_json(ORGAN_INDEX_PATH, index)

def camel_case(name):
    parts = name.replace("_", " ").replace("-", " ").split()
    return "".join(p.capitalize() for p in parts)

def auto_generate_organ_index():
    """
    Scans organs/ and generates CamelCase names automatically.
    Manual overrides in organ_index.json always win.
    """
    index = load_organ_index()
    changed = False

    for file in ORGANS_DIR.iterdir():
        if file.is_file() and file.suffix == ".py":
            filename = file.stem  # e.g., calm_pressure
            auto_name = camel_case(filename)

            # If user already manually named it, skip
            if filename in index:
                continue

            index[filename] = auto_name
            changed = True

    if changed:
        save_organ_index(index)

    return index

def list_organs():
    index = auto_generate_organ_index()
    header("📦 ORGANS")
    for filename, name in index.items():
        print(f"{name}  →  {filename}.py")

def resolve_organ_name(query):
    """
    Fuzzy match against CamelCase organ names.
    """
    index = auto_generate_organ_index()
    names = list(index.values())
    match = fuzzy_match(query, names)
    return match

def open_organ(name):
    """
    Opens the organ file in nano.
    """
    index = auto_generate_organ_index()

    # Find filename for this organ name
    for filename, organ_name in index.items():
        if organ_name == name:
            path = ORGANS_DIR / f"{filename}.py"
            os.system(f"nano '{path}'")
            return

    print(f"Organ not found: {name}")

def register_organ(manual_name, filename):
    """
    Allows user to manually override organ name.
    """
    index = load_organ_index()
    index[filename] = manual_name
    save_organ_index(index)
    print(f"Registered organ: {manual_name} → {filename}.py")
# ==============================
# NOTE SYSTEM
# ==============================

def open_today():
    path = daily_note_path(today_str())
    if not path.exists():
        safe_write(path, f"# Daily Notes — {today_str()}\n\n")
    os.system(f"nano '{path}'")

def open_yesterday():
    date = date_days_ago(1)
    path = daily_note_path(date)
    if not path.exists():
        print(f"No note found for yesterday ({date})")
        return
    os.system(f"nano '{path}'")

def open_daily():
    """
    Alias for open_today()
    """
    open_today()

def list_archived_notes():
    header("📘 ARCHIVED DAILY NOTES")
    files = [p for p in NOTES_DIR.iterdir() if p.is_file() and p.name.startswith("daily_")]
    files = sorted(files)
    for f in files:
        print(f.name)

def show_archived_notes():
    header("📘 ARCHIVED DAILY NOTES")
    files = [p for p in NOTES_DIR.iterdir() if p.is_file() and p.name.startswith("daily_")]
    files = sorted(files)
    for f in files:
        print(f"----- {f.name} -----")
        print(safe_read(f))
        print("\n")

def show_all_notes():
    # DAILY
    header("📘 DAILY NOTES")
    for f in sorted(NOTES_DIR.iterdir()):
        if f.is_file():
            print(f"----- {f.name} -----")
            print(safe_read(f))
            print("\n")

    # META
    header("📙 META NOTES")
    for f in sorted(META_DIR.iterdir()):
        if f.is_file():
            print(f"----- {f.name} -----")
            print(safe_read(f))
            print("\n")

    # COPILOT NOTES
    header("📗 COPILOT NOTES")
    for f in sorted(COPILOT_NOTES_DIR.iterdir()):
        if f.is_file():
            print(f"----- {f.name} -----")
            print(safe_read(f))
            print("\n")

def open_note_by_name(name):
    """
    Opens any note by filename (exact match).
    """
    # Search in all note directories
    for folder in [NOTES_DIR, META_DIR, COPILOT_NOTES_DIR]:
        path = folder / name
        if path.exists():
            os.system(f"nano '{path}'")
            return

    print(f"No note found named: {name}")
# ==============================
# SUBJECT RECALL ENGINE
# ==============================

# Stores last subject query for contextual --all
LAST_SUBJECT_QUERY = {
    "subject": None,
    "matches": []
}

def search_notes_for_subject(subject):
    """
    Case-sensitive subject search in filenames.
    Case-insensitive search in file contents.
    Returns list of matching file paths.
    """
    matches = []

    all_dirs = [NOTES_DIR, META_DIR, COPILOT_NOTES_DIR]

    for folder in all_dirs:
        for f in folder.iterdir():
            if not f.is_file():
                continue

            # Case-sensitive filename match
            if subject in f.name:
                matches.append(f)
                continue

            # Case-insensitive content match
            content = safe_read(f)
            if subject.lower() in content.lower():
                matches.append(f)

    return sorted(matches)

def show_subject_matches(matches):
    """
    Prints a selection menu for multiple matches.
    """
    header("📚 SUBJECT MATCHES")

    for i, f in enumerate(matches, 1):
        print(f"{i}. {f.name}")

    print("\nChoose a number, or type 'cancel': ", end="")
    choice = input().strip()

    if choice.lower() == "cancel":
        print("Cancelled.")
        return None

    if not choice.isdigit():
        print("Invalid choice.")
        return None

    idx = int(choice)
    if idx < 1 or idx > len(matches):
        print("Invalid selection.")
        return None

    return matches[idx - 1]

def open_subject(subject, use_all=False):
    """
    Main subject recall entrypoint.
    Handles:
    - contextual ALL
    - global ALL
    - selection menu
    """
    global LAST_SUBJECT_QUERY

    # CONTEXTUAL ALL
    if use_all and LAST_SUBJECT_QUERY["subject"] == subject:
        header(f"📚 ALL MATCHES FOR SUBJECT: {subject}")
        for f in LAST_SUBJECT_QUERY["matches"]:
            print(f"----- {f.name} -----")
            print(safe_read(f))
            print("\n")
        return

    # GLOBAL SEARCH
    matches = search_notes_for_subject(subject)

    # Update last query
    LAST_SUBJECT_QUERY["subject"] = subject
    LAST_SUBJECT_QUERY["matches"] = matches

    if not matches:
        print(f"No notes found for subject: {subject}")
        return

    # GLOBAL ALL (no previous selection)
    if use_all:
        header(f"📚 ALL MATCHES FOR SUBJECT: {subject}")
        for f in matches:
            print(f"----- {f.name} -----")
            print(safe_read(f))
            print("\n")
        return

    # SINGLE MATCH
    if len(matches) == 1:
        os.system(f"nano '{matches[0]}'")
        return

    # MULTIPLE MATCHES → SELECTION MENU
    selected = show_subject_matches(matches)
    if selected:
        os.system(f"nano '{selected}'")
# ==============================
# SUBJECT + DAY RECALL ENGINE
# ==============================

def subject_day_scope_menu(subject, target_date):
    """
    Shows the scope menu when no flags are provided.
    """
    header(f"📅 SUBJECT: {subject} — DATE: {target_date}")

    print("Choose scope:\n")
    print("1. Only this day")
    print("2. ±2 days (range)")
    print("3. All days (global subject search)")
    print("4. Cancel\n")

    choice = input("Selection: ").strip()

    if choice == "1":
        return "day"
    if choice == "2":
        return "range"
    if choice == "3":
        return "all"
    return None  # cancel or invalid


def search_subject_on_date(subject, date_str):
    """
    Searches ONLY the daily note for that date.
    """
    path = daily_note_path(date_str)
    if not path.exists():
        return []

    content = safe_read(path)
    if subject.lower() in content.lower():
        return [path]

    return []


def search_subject_range(subject, date_str):
    """
    Searches ±2 days around the target date.
    """
    base = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    results = []

    for offset in [-2, -1, 0, 1, 2]:
        d = (base + datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
        path = daily_note_path(d)
        if path.exists():
            content = safe_read(path)
            if subject.lower() in content.lower():
                results.append(path)

    return results


def open_subject_day(subject, days_ago, flag=None):
    """
    Main entrypoint for:
        memo <subject> <N> days ago
    Handles:
        - scope menu (when no flag)
        - day-only
    """
# ==============================
# HEARTBEAT SNAPSHOT + RESTORE
# ==============================

def snapshot_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def create_snapshot():
    """
    Creates a full snapshot of:
    - organs/
    - notes/
    - meta/
    - copilot_notes/
    into snapshots/<timestamp>/
    """
    ts = snapshot_timestamp()
    snap_dir = SNAPSHOTS_DIR / ts
    snap_dir.mkdir(exist_ok=True)

# Restore organs
    src_organs = snap_dir / "organs"
    if src_organs.exists():
        shutil.rmtree(ORGANS_DIR)
        shutil.copytree(src_organs, ORGANS_DIR)

    # Restore notes
    src_notes = snap_dir / "notes"
    if src_notes.exists():
        shutil.rmtree(NOTES_DIR)
        shutil.copytree(src_notes, NOTES_DIR)

    # Restore meta
    src_meta = snap_dir / "meta"
    if src_meta.exists():
        shutil.rmtree(META_DIR)
        shutil.copytree(src_meta, META_DIR)

    # Restore copilot notes
    src_copilot = snap_dir / "copilot_notes"
    if src_copilot.exists():
        shutil.rmtree(COPILOT_NOTES_DIR)
        shutil.copytree(src_copilot, COPILOT_NOTES_DIR)

    # ============================
    # LOG RESTORE EVENT
    # ============================
    timestamp = datetime.datetime.now().isoformat()
    restore_index.setdefault("restores", []).append({
        "timestamp": timestamp,
        "from": snapshot_name,
        "to": "live"
    })
    save_json(RESTORE_INDEX_PATH, restore_index)

    print(f"Snapshot {snapshot_name} restored.")
def list_snapshots():
    header("🫀 SNAPSHOTS")
    snaps = sorted([p for p in SNAPSHOTS_DIR.iterdir() if p.is_dir()])
    for s in snaps:
        print(s.name)

def restore_snapshot(snapshot_name):
    """
    Restores from snapshots/<snapshot_name>/ back into:
    - organs/
    - notes/
    - meta/
    - copilot_notes/
    """
    snap_dir = SNAPSHOTS_DIR / snapshot_name
    if not snap_dir.exists() or not snap_dir.is_dir():
        print(f"Snapshot not found: {snapshot_name}")
        return

    # Confirm
    print(f"About to restore snapshot: {snapshot_name}")
    confirm = input("Type 'RESTORE' to confirm: ").strip()
    if confirm != "RESTORE":
        print("Restore cancelled.")
        return

    # Restore organs
    src_organs = snap_dir / "organs"
    if src_organs.exists():
        shutil.rmtree(ORGANS_DIR)
        shutil.copytree(src_organs, ORGANS_DIR)

    # Restore notes
    src_notes = snap_dir / "notes"
    if src_notes.exists():
        shutil.rmtree(NOTES_DIR)
        shutil.copytree(src_notes, NOTES_DIR)

    # Restore meta
    src_meta = snap_dir / "meta"
    if src_meta.exists():
        shutil.rmtree(META_DIR)
        shutil.copytree(src_meta, META_DIR)

    # Restore copilot notes
    src_copilot = snap_dir / "copilot_notes"
    if src_copilot.exists():
        shutil.rmtree(COPILOT_NOTES_DIR)
        shutil.copytree(src_copilot, COPILOT_NOTES_DIR)

    print(f"Snapshot {snapshot_name} restored.")
# ==============================
# BUILD NUMBERING + LINEAGE LOGGING
# ==============================

BUILD_INFO_PATH = META_DIR / "build_info.json"
LINEAGE_LOG_PATH = META_DIR / "lineage_log.txt"
# ============================================================
# ORGAN REGISTRY + CANONICAL NAMING SYSTEM
# ============================================================

def load_all_organs():
    """
    Returns a sorted list of all organ filenames (without .py)
    from the organs/ directory.
    This is the authoritative source of truth.
    """
    organs = []
    for p in ORGANS_DIR.iterdir():
        if p.is_file() and p.suffix == ".py":
            organs.append(p.stem)
    return sorted(organs)


def canonical_name(filename_stem):
    """
    Returns the canonical organ name:
    - first 10 characters of the filename stem
    - no spaces
    - stable identity for all organs
    """
    name = filename_stem.replace(" ", "")
    return name[:10]

def load_build_info():
    info = load_json(BUILD_INFO_PATH, default={"build": 0})
    return info

def save_build_info(info):
    save_json(BUILD_INFO_PATH, info)

def increment_build_number(reason):
    """
    Increments build number and logs lineage event.
    """
    info = load_build_info()
    info["build"] += 1
    save_build_info(info)

    build_num = info["build"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"BUILD {build_num} — {timestamp}\n"
        f"Reason: {reason}\n"
        f"{'-'*40}\n"
    )

    safe_append(LINEAGE_LOG_PATH, entry)

    print(f"Build incremented to {build_num}")
    return build_num

def archive_build(build_num):
    """
    Archives the current state into archive/build_<num>/
    """
    dest = ARCHIVE_DIR / f"build_{build_num}"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(exist_ok=True)

    # Copy organs
    shutil.copytree(ORGANS_DIR, dest / "organs")

    # Copy notes
    shutil.copytree(NOTES_DIR, dest / "notes")

    # Copy meta
    shutil.copytree(META_DIR, dest / "meta")

    # Copy copilot notes
    shutil.copytree(COPILOT_NOTES_DIR, dest / "copilot_notes")

    print(f"Archived build {build_num} → {dest}")

def snapshot_and_archive(reason="snapshot"):
    """
    Creates a snapshot AND increments build number AND archives.
    This is the full lineage ritual.
    """
    # 1. Create snapshot
    snap = create_snapshot()

    # 2. Increment build number
    build_num = increment_build_number(reason=f"{reason} (snapshot {snap})")

    # 3. Archive build
    archive_build(build_num)

    print(f"Snapshot + Archive complete for build {build_num}")

def restore_and_log(snapshot_name):
    """
    Restores snapshot and logs lineage event.
    """
    restore_snapshot(snapshot_name)

    # Increment build number after restore
    build_num = increment_build_number(reason=f"restore from snapshot {snapshot_name}")

    # Archive the restored state
    archive_build(build_num)

    print(f"Restore + Archive complete for build {build_num}")
# ==============================
# COMMAND PARSER + ROUTER
# ==============================

def show_help():
    header("🧠 REMEMGER COMMANDS")

    print("Daily Notes:")
    print("  memo today")
    print("  memo yesterday")
    print("  memo daily")
    print("  memo archived-notes")
    print("  memo all-notes")
    print("  memo open <filename>")
    print("")
    print("Subject Recall:")
    print("  memo <subject>")
    print("  memo <subject> --all")
    print("")
    print("Subject + Day Recall:")
    print("  memo <subject> <N> days ago")
    print("  memo <subject> <N> days ago --day")
    print("  memo <subject> <N> days ago --range")
    print("  memo <subject> <N> days ago --all")
    print("")
    print("Organs:")
    print("  memo organs")
    print("  memo organ <Name>")
    print("  memo register-organ <Name> <file.py>")
    print("")
    print("Snapshots + Lineage:")
    print("  memo snapshot")
    print("  memo snapshots")
    print("  memo restore <snapshot_name>")
    print("  memo snapshot-archive")
    print("  memo restore-archive <snapshot_name>")
    print("")
    print("Help:")
    print("  memo help")
    print("")


def parse_days_ago(tokens):
    """
    Detects patterns like:
        <subject> <N> days ago
    Returns (subject, N) or None.
    """
    if len(tokens) < 4:
        return None

    # pattern: subject ... N days ago
    if tokens[-2] == "days" and tokens[-1] == "ago":
        try:
            n = int(tokens[-3])
        except:
            return None

        subject = " ".join(tokens[:-3])
        return subject, n

    return None
# ------------------------------
# MEMO HANDLER (CAT-STYLE VIEWER + OPTIONAL EDIT)
# ------------------------------
def handle_memo(tokens):
    if not tokens:
        print("Usage: memo <today|yesterday|daily> [edit]")
        return

    sub = tokens[0]
    mode = tokens[1] if len(tokens) > 1 else None

    # DAILY NOTES
    if sub == "daily":
        path = DAILY_NOTES_INDEX

        if mode == "edit":
            open_in_nano(path)
            return

        print(safe_read(path))
        return

    # TODAY
    if sub == "today":
        path = TODAY_NOTE_PATH

        if mode == "edit":
            open_in_nano(path)
            return

        print(safe_read(path))
        return

    # YESTERDAY
    if sub == "yesterday":
        path = YESTERDAY_NOTE_PATH

        if mode == "edit":
            open_in_nano(path)
            return

        print(safe_read(path))
        return

    print(f"Unknown memo command: {sub}")

# ------------------------------
    # ORGANS
    # ------------------------------
    if args[0] == "organs":
        list_organs()
        return

    if args[0] == "organ" and len(args) > 1:
        name = resolve_organ_name(args[1])
        if name:
            open_organ(name)
        else:
            print(f"No organ matches: {args[1]}")
        return

    # ------------------------------
    # VIEW ORGAN SOURCE CODE
    # ------------------------------
    if args[0] == "code" and len(args) > 1:
        organ_name = args[1]

        # Load JSON index (CamelCase → filename)
        index = auto_generate_organ_index()

        # Find filename for this organ
        for filename, name in index.items():
            if name == organ_name:
                path = ORGANS_DIR / f"{filename}.py"
                print(f"----- {filename}.py -----")
                print(safe_read(path))
                return

        print(f"Organ not found: {organ_name}")
        return# ------------------------------
    # HELP
    # ------------------------------
    if args[0] == "help":
        show_help()
        return

    # ------------------------------
    # MEMO ROUTER
    # ------------------------------
    if args[0] == "memo":
        handle_memo(args[1:])
        return

    # ------------------------------
    # DAILY NOTES
    # ------------------------------
    if args[0] == "archived-notes":
        show_archived_notes()
        return

    if args[0] == "all-notes":
        show_all_notes()
        return

    if args[0] == "open" and len(args) > 1:
        open_note_by_name(args[1])
        return
# ------------------------------
# ORGAN LOADER (index.json → live organ instances)
# ------------------------------
import importlib
import json
from pathlib import Path

# Path to the organs folder (relative to rememger.py)
ORGANS_DIR = Path(__file__).parent / "organs"


def load_organ_index():
    """
    Load the organ index JSON file.

    Maps standardized organ names → filenames.
    Example:
        {
            "StmOrgan": "stm_organ.py",
            "CalmPressure": "calm_pressure.py",
            "HeartOrgan": "heart_organ.py",
            "WorldOrgan": "world_organ.py"
        }

    This file is the single source of truth for:
    - organ names
    - filenames
    - dynamic loading
    - viewer resolution
    """
    index_path = ORGANS_DIR / "index.json"

    if index_path.exists():
        try:
            with open(index_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading organ index:", e)
            return {}

    return {}


def load_organs_from_index(organ_index):
    """
    Dynamically import and instantiate all organs listed in index.json.

    Returns a dictionary of LIVE organ instances:
        {
            "StmOrgan": <STMOrgan instance>,
            "CalmPressure": <PressureCore instance>,
            "HeartOrgan": <HeartOrgan instance>,
            "WorldOrgan": <WorldOrgan instance>,
            ...
        }

    This is the bridge between:
    - your JSON index
    - your organs folder
    - your creature's runtime
    """
    organs = {}

    for organ_name, filename in organ_index.items():
        module_name = filename.replace(".py", "")

        try:
            # Import module: organs.stm_organ, organs.calm_pressure, etc.
            module = importlib.import_module(f"organs.{module_name}")

            # Class name matches the key in index.json
            cls = getattr(module, organ_name)

            # Instantiate the organ
            organs[organ_name] = cls()

        except Exception as e:
            print(f"Failed to load organ {organ_name} from {filename}: {e}")

    return organs


# ------------------------------
# JSON ORGAN LOADING AT STARTUP
# ------------------------------
def load_all_organs():
    """
    Convenience wrapper used by main():
    Loads the JSON index and returns live organ instances.
    """
    organ_index = load_organ_index()
    organs = load_organs_from_index(organ_index)

    print("Loaded organs:", list(organs.keys()))
    return organs
    # ------------------------------
    # SUBJECT RECALL
    # ------------------------------
    if "--all" in args:
        subject = " ".join(a for a in args if a != "--all")
        open_subject(subject, use_all=True)
        return

    # default subject recall
    subject = " ".join(args)
    open_subject(subject)
    return


if __name__ == "__main__":
    main()
