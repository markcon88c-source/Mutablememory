class PressureCore:
    """
    Calm rises when storm, alert, symbolic overload, or drift instability are high.
    Calm also rises when stability is low (self‑soothing).
    Calm falls when concentration is high (focused, not calming).
    Moves incrementally toward a mood‑modulated target.
    """

    def __init__(self):
        self.value = 0.0
        self.last_drift = 0.0

    def compute(self, state):
        p = state["pressures"]
        drift = state["drift"]["intensity"]
        mood = state["mood"]

        symbolic = p["symbolic"]
        alert = p["alert"]
        storm = p["storm"]
        concentration = p["concentration"]

        valence = mood["valence"]
        arousal = mood["arousal"]
        stability = mood["stability"]

        # -----------------------------
        # DRIFT INSTABILITY
        # -----------------------------
        drift_instability = abs(drift - self.last_drift)
        self.last_drift = drift

        # -----------------------------
        # UPWARD FORCES (calm increases)
        # -----------------------------
        up = (
            0.40 * storm +
            0.30 * alert +
            0.25 * symbolic +
            0.20 * drift_instability +
            0.20 * (1.0 - stability)
        )

        # -----------------------------
        # DOWNWARD FORCES (calm decreases)
        # -----------------------------
        down = (
            0.30 * concentration +
            0.20 * arousal +
            0.10 * valence
        )

        # -----------------------------
        # TARGET CALM VALUE
        # -----------------------------
        target = up - down
        target = max(0.0, min(1.0, target))

        # -----------------------------
        # INCREMENTAL MOVEMENT
        # -----------------------------
        gain = 0.12 + 0.10 * (1.0 - arousal)
        gain = max(0.05, min(0.25, gain))

        self.value = self.value + (target - self.value) * gain
        self.value = max(0.0, min(1.0, self.value))

        calm_value = round(self.value, 2)

        # -----------------------------
        # RETURN PACKET
        # -----------------------------
        return {
            "calm": calm_value,
            "symbolic": symbolic,
            "alert": alert,
            "storm": storm,
            "concentration": concentration
        }
