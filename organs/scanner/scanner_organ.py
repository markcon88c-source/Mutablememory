#!/usr/bin/env python3
import os

ORGANS_DIR = "organs"

def scan_for_organs():
    """
    SCAN_FOR_ORGANS
    ----------------
    Returns a sorted list of organ names by scanning the filesystem.

    Rules:
      - Only directories inside 'organs/' count as organs
      - Inside each organ directory, look for:
            <name>.py
            <name>_organ.py
      - If either exists, the organ is valid
    """
    found = []

    if not os.path.exists(ORGANS_DIR):
        return found

    for name in os.listdir(ORGANS_DIR):
        organ_path = os.path.join(ORGANS_DIR, name)
        if not os.path.isdir(organ_path):
            continue

        # Pattern A: <name>_organ.py
        organ_file_a = os.path.join(organ_path, f"{name}_organ.py")

        # Pattern B: <name>.py
        organ_file_b = os.path.join(organ_path, f"{name}.py")

        if os.path.exists(organ_file_a) or os.path.exists(organ_file_b):
            found.append(name)

    return sorted(found)
