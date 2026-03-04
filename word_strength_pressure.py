# word_strength_pressure.py

class WordStrengthPressure:
    """
    Word strength rises with symbolic meaning, storm activity, and positive valence.
    It moves incrementally toward a mood‑modulated target.
    """

    def compute(self, state):
        pressures = state["pressures"]
        mood = state["mood"]

        current = pressures["word_strength"]

        symbolic = pressures["symbolic"]
        storm = pressures["storm"]
        calm = pressures["calm"]

        valence = mood.get("valence", 0.5)
        arousal = mood.get("arousal", 0.5)
        stability = mood.get("stability", 0.5)

        # Target word strength:
        # - high when symbolic is high
        # - high when storm is active
        # - boosted by positive valence
        # - slightly boosted by arousal (energy)
        # - reduced by excessive calm or stability
        target = (
            0.45 * symbolic +
            0.30 * storm +
            0.15 * valence +
            0.10 * arousal -
            0.05 * calm -
            0.05 * stability
        )

        # Clamp target to [0, 1]
        if target < 0.0:
            target = 0.0
        if target > 1.0:
            target = 1.0

        # Gain:
        # Word strength grows faster with arousal (energetic mind)
        gain = 0.10 + 0.20 * arousal

        new_value = current + (target - current) * gain

        if new_value < 0.0:
            new_value = 0.0
        if new_value > 1.0:
            new_value = 1.0

        return round(new_value, 2)