# L-LEVEL VIEWER — CATHEDRAL EDITION
# Displays the creature's L-levels for debugging and heartbeat output.

class LLevelViewer:
    def __init__(self):
        self.last_levels = None

    def tick(self, creature=None):
        # If the creature has an L-level organ, pull from it
        if creature and hasattr(creature, "llevels"):
            try:
                self.last_levels = creature.llevels.get_levels()
            except:
                pass
        return self.last_levels

    def show(self):
        return {
            "llevels": self.last_levels
        }
