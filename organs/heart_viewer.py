# HEART VIEWER — CATHEDRAL EDITION
# Displays the creature's heartbeat, pulse, and iteration rhythm.

class HeartViewer:
    def __init__(self, creature):
        self.creature = creature
        self.snapshot = {}

    def tick(self):
        snap = {}

        # Heartbeat counter
        if hasattr(self.creature, "heartbeat"):
            try:
                snap["heartbeat"] = self.creature.heartbeat
            except:
                snap["heartbeat"] = None

        # Pulse or beat strength
        if hasattr(self.creature, "pulse"):
            try:
                snap["pulse"] = self.creature.pulse
            except:
                snap["pulse"] = None

        # Iteration count
        if hasattr(self.creature, "iteration"):
            try:
                snap["iteration"] = self.creature.iteration
            except:
                snap["iteration"] = None

        self.snapshot = snap
        return snap

    def show(self):
        return dict(self.snapshot)
