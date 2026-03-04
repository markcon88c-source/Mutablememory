# main_support/loader.py

import importlib

_loaded = set()

def load_main(module_name):
    """
    Safely loads another main module without recursion or crashes.
    Returns the module's main() function if available.
    """

    if module_name in _loaded:
        print(f"[MainSupport] {module_name} already loaded — skipping to avoid recursion.")
        return None

    print(f"[MainSupport] Loading alternate main: {module_name}")
    _loaded.add(module_name)

    mod = importlib.import_module(module_name)

    if hasattr(mod, "main"):
        return mod.main
    else:
        print(f"[MainSupport] {module_name} has no main() function.")
        return None
