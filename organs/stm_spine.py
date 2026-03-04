# ============================================================
# STMSpine — Short-Term Memory Spine Organ
# ============================================================

class STMSpineOrgan:
    """
    Provides structural support for STM processes.
    Tracks load, tension, and coherence of short-term memory.
    """

    def __init__(self, creature):
        self.creature = creature
        self.load = 0
        self.tension = 0
        self.coherence = 1.0

    def tick(self):
        # Simple placeholder physiology
        self.load = (self.load + 1) % 10
        self.tension = (self.tension + 0.1) % 5
        self.coherence = max(0.0, 1.0 - (self.tension * 0.05))
        return []

    def snapshot(self):
        return {
            "load": self.load,
            "tension": self.tension,
            "coherence": self.coherence,
        }

# Alias required by import_wall_experimental and all_organs
STMSpine = STMSpineOrgan
