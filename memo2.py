#!/usr/bin/env python3

import sys
import os
import subprocess
from datetime import datetime


def show_help():
    print("memo2 commands:")
    print("  daily                 Show today's daily note")
    print("  daily edit            Edit today's daily note")
    print("  recall <subject>      Recall all dailies, notes, goals, and organs for subject")
    print("  grep <pattern>        Grep critter, save results to text file")
    print("  everything            Dump all memory artifacts")
    print("  help                  Show this help message")


def handle_daily(args):
    from organs.daily.daily_organ import DailyOrgan
    organ = DailyOrgan()

    if len(args) > 1 and args[1] == "edit":
        organ.edit_today()
    else:
        organ.show_today()


def handle_recall(args):
    if len(args) < 2:
        print("Usage: memo2 recall <subject>")
        return

    subject = args[1].lower()

    daily_dir = "/storage/emulated/0/MutableMemory/critter/daily"
    notes_dir = "/storage/emulated/0/MutableMemory/critter/notes"
    goals_dir = "/storage/emulated/0/MutableMemory/critter/goals"
    organs_dir = "/storage/emulated/0/MutableMemory/critter/organs"

    matches = []

    # DAILIES
    if os.path.isdir(daily_dir):
        for filename in sorted(os.listdir(daily_dir)):
            if filename.endswith(".md"):
                path = os.path.join(daily_dir, filename)
                with open(path, "r") as f:
                    content = f.read()
                    if f"subject: {subject}" in content.lower():
                        matches.append((f"DAILY: {filename}", content))

    # NOTES
    if os.path.isdir(notes_dir):
        for filename in sorted(os.listdir(notes_dir)):
            if filename.endswith(".md") or filename.endswith(".txt"):
                path = os.path.join(notes_dir, filename)
                with open(path, "r") as f:
                    content = f.read()
                    if f"subject: {subject}" in content.lower():
                        matches.append((f"NOTE: {filename}", content))

    # GOALS
    if os.path.isdir(goals_dir):
        for filename in sorted(os.listdir(goals_dir)):
            if filename.endswith(".md") or filename.endswith(".txt"):
                path = os.path.join(goals_dir, filename)
                with open(path, "r") as f:
                    content = f.read()
                    if f"subject: {subject}" in content.lower():
                        matches.append((f"GOAL: {filename}", content))

    # RELEVANT ORGANS (name + code)
    if os.path.isdir(organs_dir):
        for filename in sorted(os.listdir(organs_dir)):
            if filename.endswith(".py"):
                path = os.path.join(organs_dir, filename)
                with open(path, "r") as f:
                    content = f.read()
                    if subject in content.lower():
                        matches.append((f"ORGAN: {filename}", content))

    if not matches:
        print(f"No entries found for subject: {subject}")
        return

    for label, content in matches:
        print(f"\n===== {label} =====\n")
        print(content)


def handle_grep(args):
    if len(args) < 2:
        print("Usage: memo2 grep <pattern>")
        return

    pattern = args[1]
    search_dir = "/storage/emulated/0/MutableMemory/critter"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_pattern = "".join(c for c in pattern if c.isalnum() or c in ("-", "_"))
    out_path = f"/storage/emulated/0/MutableMemory/critter/grep_{safe_pattern}_{timestamp}.txt"

    with open(out_path, "w") as f:
        subprocess.call(["grep", "-Rin", pattern, search_dir], stdout=f)

    print(f"Grep saved to: {out_path}")


def handle_everything():
    memory_dirs = [
        "/storage/emulated/0/MutableMemory/critter/daily",
        "/storage/emulated/0/MutableMemory/critter/notes",
        "/storage/emulated/0/MutableMemory/critter/goals",
        "/storage/emulated/0/MutableMemory/critter",
    ]

    collected = []

    for mdir in memory_dirs:
        if os.path.isdir(mdir):
            for filename in sorted(os.listdir(mdir)):
                if filename.endswith(".md") or filename.endswith(".txt"):
                    path = os.path.join(mdir, filename)
                    try:
                        with open(path, "r") as f:
                            content = f.read()
                            collected.append((filename, content))
                    except:
                        pass

    if not collected:
        print("No memory artifacts found.")
        return

    for filename, content in collected:
        print(f"\n===== {filename} =====\n")
        print(content)


def main():
    args = sys.argv[1:]

    if not args:
        show_help()
        return

    cmd = args[0]

    if cmd == "help":
        show_help()
    elif cmd == "daily":
        handle_daily(args)
    elif cmd == "recall":
        handle_recall(args)
    elif cmd == "grep":
        handle_grep(args)
    elif cmd == "everything":
        handle_everything()
    else:
        print(f"Unknown command: {cmd}")
        print("Use: memo2 help")


if __name__ == "__main__":
    main()
