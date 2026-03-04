# CATHEDRAL ORGAN REGISTRY — AUTO-LOADER

from organs.all_organs import *

class OrganRegistry:
    def __init__(self):
        self.organ_classes = {}

        # Scan all globals imported from all_organs.py
        for name, obj in globals().items():
            if isinstance(obj, type) and name.endswith("Organ"):
                self.organ_classes[name] = obj

    def load_all(self, creature):
        """Instantiate every organ with the creature and return a dict."""
        organs = {}
        for name, cls in self.organ_classes.items():
            try:
                organs[name] = cls(creature)
            except TypeError:
                # Some organs take no creature argument
                organs[name] = cls()
        return organs
