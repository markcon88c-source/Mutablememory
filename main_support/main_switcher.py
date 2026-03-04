# main_support/main_switcher.py

from main_support.loader import load_main

def switch_to(module_name):
    """
    Switches to another main module safely.
    """
    alt = load_main(module_name)
    if alt:
        print(f"[MainSupport] Switching to alternate main: {module_name}")
        alt()
