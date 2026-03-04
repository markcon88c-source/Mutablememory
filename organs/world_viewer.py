# WORLD VIEWER — CATHEDRAL EDITION
# Displays the creature's world state, world packets, and environmental structures.

class WorldViewer:
    def __init__(self, creature):
        self.creature = creature
        self.snapshot = {}

    def tick(self):
        snap = {}

        # World state dictionary
        if hasattr(self.creature, "world_state"):
            try:
                snap["world_state"] = dict(self.creature.world_state)
            except:
                snap["world_state"] = None

        # World packets (if your creature uses them)
        if hasattr(self.creature, "world_packets"):
            try:
                snap["world_packets"] = self.creature.world_packets
            except:
                snap["world_packets"] = None

        # General creature state
        if hasattr(self.creature, "state"):
            try:
                snap["creature_state"] = dict(self.creature.state)
            except:
                snap["creature_state"] = None

        self.snapshot = snap
        return snap

    def show(self):
        return dict(self.snapshot)
