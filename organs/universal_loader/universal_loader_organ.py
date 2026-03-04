#!/usr/bin/env python3

import os
import importlib


def camelize(name: str) -> str:
    """
    Convert snake_case or snake_case_organ into CamelCase or CamelCaseOrgan.
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


def load_all_filesystem_organs():
    """
    Load ALL organs in organs/ directory.
    This is universal and resilient.
    """

    base = os.path.dirname(os.path.abspath(__file__))
    organs_dir = os.path.join(base, "..")

    organs = {}

    for file in os.listdir(organs_dir):
        if not file.endswith(".py"):
            continue

        module_name = file[:-3]  # strip .py
        if module_name.startswith("__"):
            continue

        class_name = camelize(module_name)
        instance = safe_load(module_name, class_name)

        if instance is not None:
            organs[module_name] = instance

    return organs
