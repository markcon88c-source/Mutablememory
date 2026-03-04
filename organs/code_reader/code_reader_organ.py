#!/usr/bin/env python3

import os


ORGANS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def get_organ_code(organ_name: str):
    """
    Return the source code of an organ as a string.
    Works with flat-file organs like:
        organs/storm.py
        organs/drift.py
        organs/mood.py
    """

    # Construct path: organs/<organ_name>.py
    path = os.path.join(ORGANS_DIR, f"{organ_name}.py")

    if not os.path.isfile(path):
        return None

    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return None
