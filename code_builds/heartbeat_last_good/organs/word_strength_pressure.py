class WordStrengthPressure:
    """
    Word strength rises with concentration, symbolic clarity, positive valence,
    and emotional stability. It falls with storm, alert, and drift instability.
    Moves incrementally toward a mood‑modulated target.
    """

    def __init__(self):
        self.value = 0.20
        self.last_drift = 0.0

    def compute(self, state):
        p = state["pressures"]
        drift = state["drift"]["intensity"]
        mood = state["mood"]

        symbolic = p["symbolic"]
        concentration = p["concentration"]
        calm = p["calm"]
        storm = p["storm"]
        alert = p["alert"]

        valence = mood["valence"]
        arousal = mood["arousal"]
        stability = mood["stability"]

        # -----------------------------
        # DRIFT INSTABILITY
        # -----------------------------
        drift_instability = abs(drift - self.last_drift)
        self.last_drift = drift

        # -----------------------------
        # UPWARD FORCES (word strength increases)
        # -----------------------------
        up = (
            0.40 * concentration +     # focus strengthens language
            0.35 * symbolic +          # symbolic clarity boosts meaning
            0.25 * valence +           # positive mood strengthens expression
            0.20 * stability +         # groundedness supports coherence
            0.15 * calm                # calm supports clarity
        )

        # -----------------------------
        # DOWNWARD FORCES (word strength decreases)
        # -----------------------------
        down = (
            0.35 * storm +             # storm disrupts clarity
            0.30 * alert +             # hypervigilance fragments language
            0.25 * drift_instability + # instability breaks coherence
            0.10 * arousal             # high energy scatters focus
        )

        # -----------------------------
        # TARGET WORD STRENGTH
        # -----------------------------
        target = up - down
        target = max(0.0, min(1.0, target))

        # -----------------------------
        # INCREMENTAL MOVEMENT
        # -----------------------------
        gain = 0.10 + 0.15 * stability - 0.10 * storm
        gain = max(0.05, min(0.25, gain))

        self.value = self.value + (target - self.value) * gain
        self.value = max(0.0, min(1.0, self.value))

        return round(self.value, 2)
