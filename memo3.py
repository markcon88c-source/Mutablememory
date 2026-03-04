#!/usr/bin/env python3
import os
import sys
import shutil
import json
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

HOME = os.path.expanduser("~")

MEMO2_ROOT = os.path.join(HOME, "mutable_memory", "memo2")
DAILY_DIR = os.path.join(MEMO2_ROOT, "daily")
IDEAS_DIR = os.path.join(MEMO2_ROOT, "ideas")
NOTES_DIR = os.path.join(MEMO2_ROOT, "notes")
SNAPSHOTS_DIR = os.path.join(MEMO2_ROOT, "snapshots")
SUBJECTS_DIR = os.path.join(MEMO2_ROOT, "subjects")

CRITTER_ROOT = os.path.join(HOME, "MutableMemory", "critter")
CRITTER_ORGANS = os.path.join(CRITTER_ROOT, "organs")
CRITTER_SNAPSHOTS = os.path.join(HOME, "MutableMemory", "critter_snapshots")
CRITTER_RESTORE = os.path.join(HOME, "MutableMemory", "critter_restore")
CRITTER_BUILD_FILE = os.path.join(CRITTER_ROOT, "build_number.txt")

os.makedirs(MEMO2_ROOT, exist_ok=True)
os.makedirs(SUBJECTS_DIR, exist_ok=True)
os.makedirs(CRITTER_SNAPSHOTS, exist_ok=True)


# ============================================================
# UTILITIES
# ============================================================

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"[error reading {path}: {e}]"


def write_text(path, text):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# BUILD NUMBER HELPERS
# ============================================================

def ensure_build_number():
    ensure_dir(CRITTER_ROOT)
    if not os.path.exists(CRITTER_BUILD_FILE):
        write_text(CRITTER_BUILD_FILE, "0\n")


def get_build_number():
    ensure_build_number()
    try:
        with open(CRITTER_BUILD_FILE, "r", encoding="utf-8") as f:
            line = f.readline().strip() or "0"
        return int(line)
    except Exception:
        return 0


def bump_build_number():
    n = get_build_number() + 1
    write_text(CRITTER_BUILD_FILE, f"{n}\n")
    return n


# ============================================================
# SUBJECT SYSTEM
# ============================================================

def subject_dir(subject):
    return os.path.join(SUBJECTS_DIR, subject)


def subject_file(subject, name):
    return os.path.join(subject_dir(subject), name)


def subject_meta_path(subject):
    return subject_file(subject, "meta.json")


def load_subject_meta(subject):
    path = subject_meta_path(subject)
    if not os.path.isfile(path):
        return {
            "subject": subject,
            "created": now_str(),
            "updated": now_str(),
            "tags": [],
            "lineage": {
                "origin": f"build_{get_build_number():03d}",
                "last_modified_build": f"build_{get_build_number():03d}",
                "history": [
                    {
                        "build": f"build_{get_build_number():03d}",
                        "event": "created",
                        "timestamp": now_str()
                    }
                ]
            },
            "links": {
                "organs": [],
                "subjects": [],
                "notes": []
            },
            "stats": {
                "notes_count": 0,
                "goals_count": 0,
                "history_entries": 0
            }
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "subject": subject,
            "created": now_str(),
            "updated": now_str(),
            "tags": [],
            "lineage": {
                "origin": f"build_{get_build_number():03d}",
                "last_modified_build": f"build_{get_build_number():03d}",
                "history": []
            },
            "links": {
                "organs": [],
                "subjects": [],
                "notes": []
            },
            "stats": {
                "notes_count": 0,
                "goals_count": 0,
                "history_entries": 0
            }
        }


def save_subject_meta(subject, meta, event=None):
    meta["updated"] = now_str()
    build = f"build_{get_build_number():03d}"
    meta["lineage"]["last_modified_build"] = build
    if event:
        meta["lineage"].setdefault("history", []).append({
            "build": build,
            "event": event,
            "timestamp": now_str()
        })
    path = subject_meta_path(subject)
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def subject_everything(subject):
    sdir = subject_dir(subject)
    ensure_dir(sdir)

    notes_path = subject_file(subject, "notes.txt")
    goals_path = subject_file(subject, "goals.txt")
    history_path = subject_file(subject, "history.txt")

    meta = load_subject_meta(subject)

    print(f"=== SUBJECT EVERYTHING: {subject} ===\n")

    print("--- NOTES ---")
    print(read_text(notes_path) or "(no notes)")
    print()

    print("--- GOALS ---")
    print(read_text(goals_path) or "(no goals)")
    print()

    print("--- HISTORY ---")
    print(read_text(history_path) or "(no history)")
    print()

    print("--- META.JSON ---")
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    print()

    print(f"--- GREP EVERYTHING (subject: {subject}) ---")
    # Simple subject-scoped grep: search for subject name in its own files
    pattern = subject.lower()
    for path in (notes_path, goals_path, history_path, subject_meta_path(subject)):
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    if pattern in line.lower():
                        print(f"{path}:{lineno}: {line.rstrip()}")
        except Exception as e:
            print(f"[subject grep] error reading {path}: {e}")


def handle_subject(argv):
    if len(argv) < 3:
        print("Usage:")
        print("  memo2 subject <subject> everything")
        print("  memo2 subject <subject> add \"text\"")
        print("  memo2 subject <subject> edit")
        print("  memo2 subject <subject> grep PATTERN")
        print("  memo2 subject <subject> goals ...")
        print("  memo2 subject help")
        return

    subcmd = argv[2]

    if subcmd == "help":
        print("SUBJECT COMMANDS")
        print("  memo2 subject <subject> everything")
        print("  memo2 subject <subject> add \"text\"")
        print("  memo2 subject <subject> edit")
        print("  memo2 subject <subject> grep PATTERN")
        print("  memo2 subject <subject> goals")
        print("  memo2 subject <subject> goals edit")
        print("  memo2 subject <subject> goals add \"text\"")
        print("  memo2 subject <subject> goals remove \"text\"")
        return

    subject = subcmd

    if len(argv) == 4 and argv[3] == "everything":
        subject_everything(subject)
        return

    # You can extend these later; they’re placeholders for now.
    print(f"[subject] command not fully implemented here: {' '.join(argv[2:])}")


# ============================================================
# CRITTER HELPERS
# ============================================================

def critter_ok():
    ok = True
    if not os.path.isdir(CRITTER_ROOT):
        print("[critter] missing critter root:", CRITTER_ROOT)
        ok = False
    if not os.path.isdir(CRITTER_ORGANS):
        print("[critter] missing organs folder:", CRITTER_ORGANS)
        ok = False
    heartbeat = os.path.join(CRITTER_ROOT, "heartbeat.py")
    main_py = os.path.join(CRITTER_ROOT, "main.py")
    if not os.path.isfile(heartbeat):
        print("[critter] missing heartbeat.py")
        ok = False
    if not os.path.isfile(main_py):
        print("[critter] missing main.py")
        ok = False
    return ok


def organ_path(organ):
    return os.path.join(CRITTER_ORGANS, f"{organ}.py")


def grep_organ_everything(organ):
    """
    GREP EVERYTHING for this organ:
      - organ code
      - organ snapshots
      - critter metadata / lineage / build
      - memo2 memory (daily/ideas/notes)
      - subjects
    """
    print(f"--- GREP EVERYTHING (organ: {organ}) ---")
    pattern = organ.lower()

    search_roots = []

    # Organ code
    opath = organ_path(organ)
    if os.path.isfile(opath):
        search_roots.append(opath)

    # Organ snapshots
    if os.path.isdir(CRITTER_SNAPSHOTS):
        search_roots.append(CRITTER_SNAPSHOTS)

    # Critter root (meta, lineage, build)
    if os.path.isdir(CRITTER_ROOT):
        search_roots.append(CRITTER_ROOT)

    # Memo2 memory roots
    for root in (DAILY_DIR, IDEAS_DIR, NOTES_DIR):
        if os.path.isdir(root):
            search_roots.append(root)

    # Subjects
    if os.path.isdir(SUBJECTS_DIR):
        search_roots.append(SUBJECTS_DIR)

    seen = set()
    matches = 0

    def grep_file(path):
        nonlocal matches
        if path in seen:
            return
        seen.add(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    if pattern in line.lower():
                        print(f"{path}:{lineno}: {line.rstrip()}")
                        matches += 1
        except Exception as e:
            print(f"[critter grep] error reading {path}: {e}")

    for root in search_roots:
        if os.path.isfile(root):
            grep_file(root)
        else:
            for r, _, files in os.walk(root):
                for name in files:
                    grep_file(os.path.join(r, name))

    if matches == 0:
        print(f"[critter grep] no matches for '{organ}'")


# ============================================================
# CRITTER ORGAN SUITE
# ============================================================

def critter_snapshot_full():
    if not critter_ok():
        return
    build = bump_build_number()
    snap_dir = os.path.join(CRITTER_SNAPSHOTS, f"build_{build:03d}")
    if os.path.exists(snap_dir):
        shutil.rmtree(snap_dir)
    shutil.copytree(CRITTER_ROOT, os.path.join(snap_dir, "critter"))
    print(f"[critter] full snapshot created: build_{build:03d}")


def critter_snapshot_organ(organ):
    if not critter_ok():
        return
    opath = organ_path(organ)
    if not os.path.isfile(opath):
        print("[critter] organ file not found:", opath)
        return
    build = bump_build_number()
    snap_dir = os.path.join(CRITTER_SNAPSHOTS, f"build_{build:03d}")
    ensure_dir(snap_dir)
    dst = os.path.join(snap_dir, f"organ_{organ}.py")
    shutil.copy2(opath, dst)
    print(f"[critter] organ snapshot created: build_{build:03d} ({organ})")


def critter_restore_full(build):
    try:
        b = int(build)
    except ValueError:
        print("[critter] invalid build:", build)
        return
    snap_dir = os.path.join(CRITTER_SNAPSHOTS, f"build_{b:03d}", "critter")
    if not os.path.isdir(snap_dir):
        print("[critter] snapshot not found:", snap_dir)
        return
    if os.path.isdir(CRITTER_ROOT):
        shutil.rmtree(CRITTER_ROOT)
    shutil.copytree(snap_dir, CRITTER_ROOT)
    bump_build_number()
    print(f"[critter] restored from build_{b:03d}")


def critter_restore_organ(organ, build):
    try:
        b = int(build)
    except ValueError:
        print("[critter] invalid build:", build)
        return
    src = os.path.join(CRITTER_SNAPSHOTS, f"build_{b:03d}", f"organ_{organ}.py")
    if not os.path.isfile(src):
        print("[critter] organ snapshot not found:", src)
        return
    opath = organ_path(organ)
    ensure_dir(os.path.dirname(opath))
    shutil.copy2(src, opath)
    bump_build_number()
    print(f"[critter] organ {organ} restored from build_{b:03d}")


def critter_everything():
    print("=== CRITTER EVERYTHING ===\n")
    print(f"Root: {CRITTER_ROOT}")
    print(f"Build: {get_build_number()}")
    print()

    if not os.path.isdir(CRITTER_ROOT):
        print("[critter] critter root missing")
        return

    print("--- ORGANS ---")
    if os.path.isdir(CRITTER_ORGANS):
        for name in sorted(os.listdir(CRITTER_ORGANS)):
            path = os.path.join(CRITTER_ORGANS, name)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                print(f"{name} ({size} bytes)")
    else:
        print("(no organs)")
    print()

    print("--- SNAPSHOTS ---")
    if os.path.isdir(CRITTER_SNAPSHOTS):
        for name in sorted(os.listdir(CRITTER_SNAPSHOTS)):
            print(name)
    else:
        print("(no snapshots)")
    print()

    print("--- HEARTBEAT CHECK ---")
    critter_ok()
    print()

    print("--- GREP EVERYTHING (critter) ---")
    # Simple critter-wide grep hook: search for the word "organ" in critter tree
    pattern = "organ"
    for root in (CRITTER_ROOT,):
        for r, _, files in os.walk(root):
            for fname in files:
                path = os.path.join(r, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for lineno, line in enumerate(f, start=1):
                            if pattern in line.lower():
                                print(f"{path}:{lineno}: {line.rstrip()}")
                except Exception as e:
                    print(f"[critter grep] error reading {path}: {e}")


def critter_organ_everything(organ):
    print(f"=== ORGAN EVERYTHING: {organ} ===\n")

    opath = organ_path(organ)
    print("--- ORGAN CODE ---")
    if os.path.isfile(opath):
        print(read_text(opath) or "(empty)")
    else:
        print("[critter] organ file not found:", opath)
    print()

    print("--- ORGAN SNAPSHOTS ---")
    if os.path.isdir(CRITTER_SNAPSHOTS):
        for name in sorted(os.listdir(CRITTER_SNAPSHOTS)):
            bdir = os.path.join(CRITTER_SNAPSHOTS, name)
            if not os.path.isdir(bdir):
                continue
            for fname in sorted(os.listdir(bdir)):
                if fname == f"organ_{organ}.py":
                    print(os.path.join(name, fname))
    else:
        print("(no snapshots)")
    print()

    grep_organ_everything(organ)


def handle_critter(argv):
    if len(argv) < 3:
        print("CRITTER COMMANDS")
        print("  memo2 critter heartbeat")
        print("  memo2 critter bring-back")
        print("  memo2 critter snapshot")
        print("  memo2 critter snapshot organ <organ>")
        print("  memo2 critter restore <build>")
        print("  memo2 critter restore organ <organ> <build>")
        print("  memo2 critter everything")
        print("  memo2 critter organ <organ> everything")
        print("  memo2 critter help")
        return

    action = argv[2]

    if action == "help":
        print("CRITTER COMMANDS")
        print("  memo2 critter heartbeat")
        print("  memo2 critter bring-back")
        print("  memo2 critter snapshot")
        print("  memo2 critter snapshot organ <organ>")
        print("  memo2 critter restore <build>")
        print("  memo2 critter restore organ <organ> <build>")
        print("  memo2 critter everything")
        print("  memo2 critter organ <organ> everything")
        return

    if action == "heartbeat":
        if critter_ok():
            print("[critter] heartbeat OK")
            print(f"[critter] build number: {get_build_number()}")
        return

    if action == "bring-back":
        if not os.path.isdir(CRITTER_RESTORE):
            print("[critter] restore folder not found:", CRITTER_RESTORE)
            return
        if os.path.isdir(CRITTER_ROOT):
            shutil.rmtree(CRITTER_ROOT)
        shutil.copytree(CRITTER_RESTORE, CRITTER_ROOT)
        print("[critter] restored from critter_restore")
        return

    if action == "snapshot":
        if len(argv) >= 4 and argv[3] == "organ":
            if len(argv) < 5:
                print("Usage: memo2 critter snapshot organ <organ>")
                return
            organ = argv[4]
            critter_snapshot_organ(organ)
        else:
            critter_snapshot_full()
        return

    if action == "restore":
        if len(argv) >= 4 and argv[3] == "organ":
            if len(argv) < 6:
                print("Usage: memo2 critter restore organ <organ> <build>")
                return
            organ = argv[4]
            build = argv[5]
            critter_restore_organ(organ, build)
        else:
            if len(argv) < 4:
                print("Usage: memo2 critter restore <build>")
                return
            build = argv[3]
            critter_restore_full(build)
        return

    if action == "everything":
        critter_everything()
        return

    if action == "organ":
        if len(argv) < 5:
            print("Usage: memo2 critter organ <organ> everything")
            return
        organ = argv[3]
        sub = argv[4]
        if sub == "everything":
            critter_organ_everything(organ)
            return
        print(f"[critter] unknown organ subcommand: {sub}")
        return

    print(f"[critter] unknown action: {action}")


# ============================================================
# CODE SUMMONING
# ============================================================

def handle_code(argv):
    if len(argv) < 3:
        print("Usage: memo2 code <organ>")
        return
    organ = argv[2]
    opath = organ_path(organ)
    print(f"=== ORGAN CODE: {organ} ===")
    print(f"Path: {opath}")
    if not os.path.isfile(opath):
        print("[code] organ file not found")
        return
    print()
    print(read_text(opath) or "(empty)")


# ============================================================
# EVERYTHING (GLOBAL) + HELP
# ============================================================

def handle_everything(argv):
    print("=== MEMO2 EVERYTHING (GLOBAL) ===\n")

    print("--- DAILY ---")
    print(f"Dir: {DAILY_DIR}")
    print()

    print("--- IDEAS ---")
    print(f"Dir: {IDEAS_DIR}")
    print()

    print("--- NOTES ---")
    print(f"Dir: {NOTES_DIR}")
    print()

    print("--- SUBJECTS ---")
    if os.path.isdir(SUBJECTS_DIR):
        for name in sorted(os.listdir(SUBJECTS_DIR)):
            print(name)
    else:
        print("(no subjects)")
    print()

    print("--- CRITTER ---")
    print(f"Root: {CRITTER_ROOT}")
    print(f"Build: {get_build_number()}")
    print()

    print("--- GREP EVERYTHING (global) ---")
    # Simple global grep hook: search for the word "subject" in memo2 tree
    pattern = "subject"
    for root in (MEMO2_ROOT,):
        for r, _, files in os.walk(root):
            for fname in files:
                path = os.path.join(r, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for lineno, line in enumerate(f, start=1):
                            if pattern in line.lower():
                                print(f"{path}:{lineno}: {line.rstrip()}")
                except Exception as e:
                    print(f"[global grep] error reading {path}: {e}")


def handle_help(argv):
    print("memo2 — modular memory & critter router\n")
    print("GENERAL")
    print("  memo2 daily ...")
    print("  memo2 grep PATTERN")
    print("  memo2 autosave")
    print("  memo2 restore SNAPSHOT SCOPE")
    print("  memo2 restore-full SNAPSHOT")
    print("  memo2 everything")
    print()
    print("SUBJECTS")
    print("  memo2 subject <subject> everything")
    print("  memo2 subject <subject> ...")
    print("  memo2 subject help")
    print()
    print("CRITTER")
    print("  memo2 critter heartbeat")
    print("  memo2 critter bring-back")
    print("  memo2 critter snapshot")
    print("  memo2 critter snapshot organ <organ>")
    print("  memo2 critter restore <build>")
    print("  memo2 critter restore organ <organ> <build>")
    print("  memo2 critter everything")
    print("  memo2 critter organ <organ> everything")
    print("  memo2 critter help")
    print()
    print("CODE")
    print("  memo2 code <organ>")


# ============================================================
# PLACEHOLDER HANDLERS FOR EXISTING ORGANS
# ============================================================

def handle_daily(argv):
    print("[daily] not implemented in this example file")


def handle_grep(argv):
    print("[grep] not implemented in this example file")


def handle_autosave(argv):
    print("[autosave] not implemented in this example file")


def handle_restore(argv):
    print("[restore] not implemented in this example file")


def handle_restore_full(argv):
    print("[restore-full] not implemented in this example file")


def fallback_to_rememger2(argv):
    print("[fallback] unknown command; would delegate to rememger2 here")


# ============================================================
# MAIN ROUTER
# ============================================================

def main(argv):
    if len(argv) < 2:
        handle_help(argv)
        return

    cmd = argv[1]

    if cmd == "daily":
        handle_daily(argv)
    elif cmd == "grep":
        handle_grep(argv)
    elif cmd == "autosave":
        handle_autosave(argv)
    elif cmd == "restore":
        handle_restore(argv)
    elif cmd == "restore-full":
        handle_restore_full(argv)
    elif cmd in ("everything", "dump"):
        handle_everything(argv)
    elif cmd == "subject":
        handle_subject(argv)
    elif cmd == "critter":
        handle_critter(argv)
    elif cmd == "code":
        handle_code(argv)
    elif cmd in ("help", "-h", "--help"):
        handle_help(argv)
    else:
        fallback_to_rememger2(argv)


if __name__ == "__main__":
    main(sys.argv)
