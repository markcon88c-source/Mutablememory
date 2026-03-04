# WORLD ORGAN — baseline version
# This organ currently acts as a placeholder for world-state.
# It must accept the bus/creature argument so the Cathedral can instantiate it.

class WorldOrgan:
    def __init__(self, bus):
        # Required so CathedralCreature can pass self.bus
        self.bus = bus

        # Preserve any existing world-state fields you had before
        self.state = {}
        self.cycle = 0

    def tick(self):
        # Placeholder tick — does nothing yet
        # Future physiology (world-state, cycles, pressure, etc.) can be added later
        self.cycle += 1
        pass
