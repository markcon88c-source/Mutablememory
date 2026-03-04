# drift.py

class DriftOrgan:
    def __init__(self):
        self.intensity = 0.0
        self.tone = "neutral"
        self.reason = "none"

    def compute(self, state):
        pressures = state["pressures"]

        symbolic = pressures["symbolic"]
        storm = pressures["storm"]
        alert = pressures["alert"]
        calm = pressures["calm"]
        concentration = pressures["concentration"]
        word_strength = pressures["word_strength"]

        # ------------------------------------------------------------
        # HYBRID DRIFT MODEL (Option C)
        # ------------------------------------------------------------
        # Upward forces (instability)
        up = (
            storm * 0.50 +
            alert * 0.30 +
            symbolic * 0.10 +
            word_strength * 0.10
        )

        # Downward forces (stability)
        down = (
            calm * 0.30 +
            concentration * 0.30
        )

        # Target drift = instability minus stability
        target = up - down

        # Normalize target into 0–1 range
        if target < 0.0:
            target = 0.0
        if target > 1.0:
            target = 1.0

        # ------------------------------------------------------------
        # Move intensity toward target smoothly
        # ------------------------------------------------------------
        self.intensity = self.intensity + (target - self.intensity) * 0.15

        # ------------------------------------------------------------
        # Natural decay to prevent sticking
        # ------------------------------------------------------------
        self.intensity = self.intensity * 0.98

        # Clamp
        if self.intensity < 0.0:
            self.intensity = 0.0
        if self.intensity > 1.0:
            self.intensity = 1.0

        # ------------------------------------------------------------
        # Tone logic
        # ------------------------------------------------------------
        if self.intensity > 0.60:
            self.tone = "rising"
        elif self.intensity < 0.30:
            self.tone = "falling"
        else:
            self.tone = "steady"

        self.reason = "instability vs stability blend"

        return {
            "intensity": round(self.intensity, 2),
            "tone": self.tone,
            "reason": self.reason
        }




