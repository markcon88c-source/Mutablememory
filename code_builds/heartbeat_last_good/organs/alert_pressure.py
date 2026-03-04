class AlertPressure:
    """
    Alert rises with storm, drift instability, symbolic overload, and low stability.
    Alert falls with calm, concentration, and positive valence.
    Moves incrementally toward a mood‑modulated target.
    """

    def __init__(self):
        self.value = 0.10
        self.last_drift = 0.0

    def compute(self, state):
        p = state["pressures"]
        drift = state["drift"]["intensity"]
        mood = state["mood"]

        symbolic = p["symbolic"]
        calm = p["calm"]
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
        # UPWARD FORCES (alert increases)
        # -----------------------------
        up = (
            0.40 * storm +             # storm heightens vigilance
            0.30 * drift_instability + # instability triggers scanning
            0.25 * symbolic +          # symbolic overload = threat ambiguity
            0.20 * (1.0 - stability) + # low stability = hypervigilance
            0.15 * arousal             # high energy fuels alertness
        )

        # -----------------------------
        # DOWNWARD FORCES (alert decreases)
        # -----------------------------
        down = (
            0.35 * calm +              # calm suppresses alert
            0.25 * concentration +     # focus reduces scanning
            0.15 * valence             # positive mood reduces threat bias
        )

        # -----------------------------
        # TARGET ALERT VALUE
        # -----------------------------
        target = up - down
        target = max(0.0, min(1.0, target))

        # -----------------------------
        # INCREMENTAL MOVEMENT
        # -----------------------------
        gain = 0.15 + 0.20 * arousal - 0.10 * stability
        gain = max(0.05, min(0.30, gain))

        self.value = self.value + (target - self.value) * gain
        self.value = max(0.0, min(1.0, self.value))

        return round(self.value, 2)
