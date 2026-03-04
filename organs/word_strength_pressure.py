# organs/word_strength_pressure.py
# Modern WordStrengthPressure organ compatible with new drift format

class WordStrengthPressure:
    def __init__(self):
        self.value = 0.0
        self.last_drift = 0.0

    def _to_float(self, x, default=0.0):
        try:
            return float(x)
        except Exception:
            return default

    def compute(self, state):
        pressures = state.get("pressures", {})
        if not isinstance(pressures, dict):
            pressures = {}

        # NEW: drift is a float, not a dict
        raw_drift = state.get("drift", 0.0)
        drift = self._to_float(raw_drift, 0.0)

        calm = self._to_float(pressures.get("calm", 0.0))
        storm = self._to_float(pressures.get("storm", 0.0))
        symbolic = self._to_float(pressures.get("symbolic", 0.0))
        concentration = self._to_float(pressures.get("concentration", 0.0))

        # Drift instability → weakens word strength
        drift_delta = abs(drift - self.last_drift)
        self.last_drift = drift
        instability_penalty = drift_delta * 0.30

        # Symbolic clarity + concentration → strengthen words
        clarity_bonus = symbolic * 0.35 + concentration * 0.30

        # Calm helps stabilize word strength
        calm_bonus = calm * 0.20

        # Storm disrupts word strength
        storm_penalty = storm * 0.25

        increase = clarity_bonus + calm_bonus
        decrease = instability_penalty + storm_penalty + 0.05  # decay

        self.value += increase
        self.value -= decrease

        # Gentle pull toward mid‑range
        target = 0.45
        self.value += (target - self.value) * 0.05

        # Clamp
        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        return self.value
