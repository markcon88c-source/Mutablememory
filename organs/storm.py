# =========================================================
# storm.py — StormOrgan (Emotional Storm Engine)
# =========================================================

import math

class StormOrgan:
    def __init__(self):
        # The internal storm value (0.0–1.0)
        self.value = 0.20

    # -----------------------------------------------------
    # DRIFT FUNCTIONS (used by main.py)
    # -----------------------------------------------------
    def intensity(self, tick):
        """
        Drift intensity used by main.py.
        Smooth oscillation between 0.0 and 1.0.
        """
        return (math.sin(tick / 8.0) + 1) / 2

    def tone(self, tick):
        """
        Drift tone used by main.py.
        Alternates between 'rising' and 'falling'.
        """
        return "rising" if math.sin(tick / 12.0) > 0 else "falling"

    # -----------------------------------------------------
    # MAIN STORM COMPUTATION (mood + pressures)
    # -----------------------------------------------------
    def compute(self, state):
        """
        Computes the storm value based on:
        - symbolic pressure
        - alert pressure
        - calm pressure
        - concentration pressure
        - drift intensity
        """

        p = state["pressures"]
        drift = state["drift"]["intensity"]

        symbolic = p["symbolic"]
        alert = p["alert"]
        calm = p["calm"]
        concentration = p["concentration"]

        # -----------------------------
        # UPWARD FORCES (stronger)
        # -----------------------------
        up = 0.0
        up += symbolic * 0.40
        up += alert * 0.50
        up += drift * 0.60

        # -----------------------------
        # DOWNWARD FORCES (weaker)
        # -----------------------------
        down = 0.0
        down += calm * 0.20
        down += concentration * 0.20

        # -----------------------------
        # NEW STORM VALUE
        # -----------------------------
        target = up - down

        if target < 0.0:
            target = 0.0
        if target > 1.0:
            target = 1.0

        # Smooth movement toward target
        self.value = self.value + (target - self.value) * 0.30

        # Clamp
        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        return round(self.value, 2)
