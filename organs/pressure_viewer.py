# PRESSURE VIEWER — CATHEDRAL EDITION
# Displays symbolic pressure, calm pressure, and core pressure.

class PressureViewer:
    def __init__(self):
        self.snapshot = {}

    def tick(self, creature=None):
        snap = {}

        # Symbolic pressure
        if creature and hasattr(creature, "symbolic_pressure"):
            try:
                snap["symbolic"] = creature.symbolic_pressure.get_pressure()
            except:
                snap["symbolic"] = None

        # Calm pressure
        if creature and hasattr(creature, "calm_pressure"):
            try:
                snap["calm"] = creature.calm_pressure.get_pressure()
            except:
                snap["calm"] = None

        # Core pressure
        if creature and hasattr(creature, "pressure_core"):
            try:
                snap["core"] = creature.pressure_core.get_pressure()
            except:
                snap["core"] = None

        self.snapshot = snap
        return snap

    def show(self):
        return dict(self.snapshot)
