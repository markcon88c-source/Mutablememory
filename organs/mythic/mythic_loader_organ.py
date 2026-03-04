#!/usr/bin/env python3

import importlib


def camelize(name: str) -> str:
    """
    Convert snake_case or snake_case_organ into CamelCase or CamelCaseOrgan.
    Examples:
        "storm" -> "Storm"
        "calm_pressure" -> "CalmPressure"
        "storm_thought_organ" -> "StormThoughtOrgan"
    """
    parts = name.replace("_organ", "").split("_")
    base = "".join(p.capitalize() for p in parts)

    if name.endswith("_organ"):
        return base + "Organ"
    return base


def safe_load(module_name: str, class_name: str):
    """
    Try to import module_name and get class_name.
    Return an instance or None if anything fails.
    """
    try:
        mod = importlib.import_module(f"organs.{module_name}")
        cls = getattr(mod, class_name)
        return cls()
    except Exception:
        return None


def load_mythic_family():
    """
    Load Mythic-related organs from the filesystem-based organs/ layout.
    This is resilient:
      - If a module or class is missing, it is skipped.
      - Only successfully loaded organs are returned.
    """

    # These are the modules you actually have in your organs/ directory.
    # (Based on your ls output.)
    candidates = [
        "pressure",
        "calm_pressure",
        "concentration_pressure",
        "alert_pressure",
        "symbolic_pressure",
        "word_strength_pressure",
        "storm",
        "drift",
        "stm",
        "english",
        "storm_thought_organ",
        "shadow_cycle",
        "worldbuilding_organ",
        "memory_organ",
        "mood_organ",
        "thought_organ",
        "world_organ",
        "hook",
        "heart",
        "idea_core",
        "longterm_memory",
    ]

    organs = {}

    for module_name in candidates:
        class_name = camelize(module_name)
        instance = safe_load(module_name, class_name)
        if instance is not None:
            organs[module_name] = instance

    return organs




