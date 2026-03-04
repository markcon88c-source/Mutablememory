# organs/forces_organ.py
# Unified force bloodstream for the creature.
# Uses the same ForceVector as MathBlockForceCore.

from organs.math_block_force_core import ForceVector

class ForcesOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.vector = ForceVector()  # spark, drift, echo, chaos, clarity, memory, pressure

    def get_packet(self):
        """Return a dict the sentence system can safely consume."""
        return self.vector.as_dict()
