#!/usr/bin/env python3

from organs.translator.translator_organ import (
    translate_organs,
    load_all_organs
)

def make_all_organs():
    """
    MAKE_ALL_ORGANS
    ----------------
    Uses the translator to:
      1. Get the list of organ names
      2. Load all organ modules
      3. Return a dict of {name: module}

    This organ imports ALL organs with .py files,
    regardless of naming pattern.
    """
    # Step 1: get organ names from translator
    names = translate_organs()

    # Step 2: load all organ modules
    modules = load_all_organs()

    # Step 3: return only the modules that match the names
    made = {name: modules[name] for name in names if name in modules}

    return made
