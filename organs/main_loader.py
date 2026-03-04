# organs/main_loader.py

import importlib

class MainLoader:
    """
    Safely loads alternate main modules without recursion.
    """

    def __init__(self):
        self.loaded = set()

    def load(self, module_name):
        if module_name in self.loaded:
            print(f"[MainLoader] {module_name} already loaded — skipping to avoid recursion.")
            return None

        print(f"[MainLoader] Loading alternate main: {module_name}")
        self.loaded.add(module_name)

        mod = importlib.import_module(module_name)

        if hasattr(mod, "main"):
            return mod.main
        else:
            print(f"[MainLoader] {module_name} has no main() function.")
            return None
