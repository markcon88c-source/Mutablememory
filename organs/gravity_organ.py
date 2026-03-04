# ============================================================
# GRAVITY ORGAN — Cathedral Edition (Aligned Version)
# ============================================================

import random

class GravityOrgan:
    """
    Maintains a narrative-gravity vector and emits a Cathedral packet
    each heartbeat. Compatible with Creature(self), tick(self, creature),
    and ViewerOrchestrator.
    """

    def __init__(self, creature):
        self.creature = creature
        self.cycle = 0
        self.last_packet = None

        self.gravity_state = {
            "pull": 0.5,
            "drift": 0.5,
            "resonance": 0.5,
            "stability": 0.5
        }

    def _update_gravity(self):
        for k in self.gravity_state:
            delta = random.uniform(-0.02, 0.02)
            self.gravity_state[k] = max(0.0, min(1.0, self.gravity_state[k] + delta))

    def tick(self, creature):
        self.cycle += 1
        self._update_gravity()

        packet = {
            "cycle": self.cycle,
            "state": dict(self.gravity_state),
            "zone": "stable" if self.gravity_state["stability"] > 0.4 else "chaotic"
        }

        self.last_packet = packet
        return packet
