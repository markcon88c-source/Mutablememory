# organs/wiring_viewer.py
# Modern WiringViewer – simple organ presence map

class WiringViewer:
    """
    Lightweight wiring viewer.
    Prints a simple map of key organs and their presence.
    """

    def __init__(self, creature):
        self.creature = creature

    def show(self):
        print("\n==============================")
        print("        WIRING VIEWER")
        print("==============================")

        organs = {
            "meaning": hasattr(self.creature, "meaning"),
            "sentence_builder": hasattr(self.creature, "sentence_builder"),
            "force_normalizer": hasattr(self.creature, "force_normalizer"),
            "integrity": hasattr(self.creature, "integrity"),
            "story_metrics": hasattr(self.creature, "story_metrics"),
            "story_viewer": hasattr(self.creature, "story_viewer"),
            "language_viewer": hasattr(self.creature, "language_viewer"),
            "pressure_viewer": hasattr(self.creature, "pressure_viewer"),
            "sentence_viewer": hasattr(self.creature, "sentence_viewer"),
        }

        for name, present in organs.items():
            status = "✅" if present else "⚪"
            print(f"{status} {name}")
