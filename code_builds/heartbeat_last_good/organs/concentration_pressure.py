class ConcentrationPressure:
    """
    Concentration rises with calm, stability, and positive valence.
    It falls with storm, alert, drift instability, and high arousal.
    Moves incrementally toward a mood‑modulated target.
    """

    def __init__(self):
        self.value = 0.30
        self.last_drift = 0.0

    def compute(self, state):
        p = state["pressures"]
        drift = state["drift"]["intensity"]
        mood = state["mood"]

        calm = p["calm"]
        storm = p["storm"]
        alert = p["alert"]
        symbolic = p["symbolic"]

        valence = mood["valence"]
        arousal = mood["arousal"]
        stability = mood["stability"]

        # -----------------------------
        # DRIFT INSTABILITY
        # -----------------------------
        drift_instability = abs(drift - self.last_drift)
        self.last_drift = drift

        # -----------------------------
        # UPWARD FORCES (concentration increases)
        # -----------------------------
        up = (
            0.40 * calm +              # calm supports focus
            0.30 * stability +         # groundedness supports attention
            0.25 * valence +           # positive mood helps focus
            0.15 * symbolic            # symbolic clarity helps attention
        )

        # -----------------------------
        # DOWNWARD FORCES (concentration decreases)
        # -----------------------------
        down = (
            0.35 * storm +             # storm disrupts focus
            0.30 * alert +             # hypervigilance scatters attention
            0.25 * drift_instability + # instability breaks focus
            0.15 * arousal             # high energy reduces sustained attention
        )

        # -----------------------------
        # TARGET CONCENTRATION VALUE
        # -----------------------------
        target = up - down
        target = max(0.0, min(1.0, target))

        # -----------------------------
        # INCREMENTAL MOVEMENT
        # -----------------------------
        gain = 0.12 + 0.10 * stability - 0.10 * storm
        gain = max(0.05, min(0.25, gain))

        self.value = self.value + (target - self.value) * gain
        self.value = max(0.0, min(1.0, self.value))

        return round(self.value, 2)

