#!/usr/bin/env python3
import os
import importlib.util

# Root directory where all organs live
ORGANS_DIR = "organs"

def scan_organs():
    """
    SCAN_ORGANS
    -----------
    Returns a dict mapping organ names to their organ file paths.

    Supports both naming patterns:
        A: <name>_organ.py
        B: <name>.py
    """
    mapping = {}

    if not os.path.exists(ORGANS_DIR):
        return mapping

    for name in os.listdir(ORGANS_DIR):
        organ_path = os.path.join(ORGANS_DIR, name)
        if not os.path.isdir(organ_path):
            continue

        # Pattern A: <name>_organ.py
        organ_file_a = os.path.join(organ_path, f"{name}_organ.py")

        # Pattern B: <name>.py
        organ_file_b = os.path.join(organ_path, f"{name}.py")

        if os.path.exists(organ_file_a):
            mapping[name] = organ_file_a
        elif os.path.exists(organ_file_b):
            mapping[name] = organ_file_b

    return mapping


def import_organ(name, path):
    """
    IMPORT_ORGAN
    ------------
    Dynamically imports an organ module from a file path.
    Returns the imported module.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_all_organs():
    """
    LOAD_ALL_ORGANS
    ----------------
    Loads all organs and returns a dict:
        { "daily": <module>, "mood": <module>, ... }
    """
    mapping = scan_organs()
    loaded = {}

    for name, path in mapping.items():
        try:
            loaded[name] = import_organ(name, path)
        except Exception as e:
            print(f"Failed to load organ '{name}': {e}")

    return loaded


def translate_organs():
    """
    TRANSLATE_ORGANS
    ----------------
    Returns a sorted list of organ names.
    """
    return sorted(scan_organs().keys())
