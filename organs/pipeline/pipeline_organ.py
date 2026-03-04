#!/usr/bin/env python3

import os
import importlib

# OLD SYSTEM (still used for scanning + translation)
from organs.scanner.scanner_organ import scan_for_organs
from organs.translator.translator_organ import translate_organs

# UNIVERSAL LOADER (new system)
from organs.universal_loader.universal_loader_organ import load_all_filesystem_organs

# MYTHIC PHYSIOLOGY
from organs.mythic.mythic_loader_organ import load_mythic_family

# CODE CACHE
from organs.code_refresh.code_refresh_organ import refresh_all_code

# CREATURE CORE
from critter.critter import Critter


# ---------------------------------------------------------
# HUMAN-READABLE NAME TRANSLATION
# ---------------------------------------------------------

def common_name(raw: str) -> str:
    parts = raw.split("_")
    return " ".join(word.capitalize() for word in parts)


def translate_all_organs(raw_list):
    return [common_name(name) for name in raw_list]


# ---------------------------------------------------------
# LOAD MAIN, AGENCY CORE, AND VIEWERS
# ---------------------------------------------------------

def load_main_and_agency():
    modules = {}
    for name in ["main", "agency_core"]:
        try:
            modules[name] = importlib.import_module(name)
        except Exception as e:
            modules[name] = f"Error loading {name}: {e}"
    return modules


def load_viewers():
    viewer_dir = "viewer"
    modules = {}

    if not os.path.isdir(viewer_dir):
        return modules

    for file in os.listdir(viewer_dir):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                modules[name] = importlib.import_module(f"viewer.{name}")
            except Exception as e:
                modules[name] = f"Error loading viewer {name}: {e}"

    return modules


# ---------------------------------------------------------
# FULL PIPELINE
# ---------------------------------------------------------

def run_pipeline():
    """
    FULL CREATURE PIPELINE
    Loads:
      - filesystem organs (universal loader)
      - mythic physiology
      - code cache
      - main + agency_core
      - viewers
      - creature assembly
    """

    # 1. Raw scan (for display only)
    scanned = scan_for_organs()

    # 2. Human-readable names
    translated_common = translate_all_organs(scanned)

    # 3. Translator mapping (legacy)
    translated_raw = translate_organs()

    # 4. UNIVERSAL FILESYSTEM ORGANS
    filesystem_organs = load_all_filesystem_organs()

    # 5. MYTHIC PHYSIOLOGY
    mythic = load_mythic_family()

    # 6. CODE CACHE
    code_cache = refresh_all_code()

    # 7. MAIN + AGENCY CORE
    main_agency = load_main_and_agency()

    # 8. VIEWERS
    viewers = load_viewers()

    # 9. ASSEMBLE CREATURE
    creature = Critter()
    creature.load_organs(filesystem_organs)
    creature.load_physiology(mythic)

    # 10. RETURN FULL STATE
    return {
        "scanned": scanned,
        "translated_common": translated_common,
        "translated_raw": translated_raw,
        "filesystem_organs": filesystem_organs,
        "mythic": mythic,
        "code_cache": code_cache,
        "main_agency": main_agency,
        "viewers": viewers,
        "creature": creature,
    }
