# organs/concentration_pressure.py
# Cathedral-spec ConcentrationPressure organ
# Focus emerges from stability, calm, symbolic resonance, and low storm.

class ConcentrationPressureOrgan:
    def __init__(self):
        self.value = 0.0
        self.last_drift = 0.0
        self.last_value = 0.0

    def _f(self, x, default=0.0):
        try:
            return float(x)
        except Exception:
            return default

    def compute(self, state):
        pressures = state.get("pressures", {}) or {}

        drift = self._f(state.get("drift", 0.0))
        calm = self._f(pressures.get("calm", 0.0))
        storm = self._f(pressures.get("storm", 0.0))
        symbolic = self._f(pressures.get("symbolic", 0.0))
        word_strength = self._f(pressures.get("word_strength", 0.0))
        mood = self._f(state.get("mood", 0.0))
        stability = self._f(state.get("stability", 0.0))

        # ------------------------------------------------------------
        # DRIFT PHYSICS
        # ------------------------------------------------------------
        drift_velocity = abs(drift - self.last_drift)
        drift_accel = abs(drift_velocity - abs(self.last_value - self.value))

        drift_penalty = (
            drift_velocity * 0.35 +
            drift_accel * 0.20
        )

        self.last_drift = drift

        # ------------------------------------------------------------
        # CALM + SYMBOLIC RESONANCE
        # ------------------------------------------------------------
        calm_bonus = calm * 0.40
        symbolic_resonance = symbolic * (0.15 + calm * 0.10)
        lexical_focus = word_strength * 0.25

        # ------------------------------------------------------------
        # STORM PHYSICS
        # ------------------------------------------------------------
        storm_penalty = storm * (0.20 + storm * 0.25)

        # ------------------------------------------------------------
        # MOOD + STABILITY
        # ------------------------------------------------------------
        mood_term = mood * 0.10
        stability_bonus = stability * 0.30

        # ------------------------------------------------------------
        # RAW UPDATE
        # ------------------------------------------------------------
        increase = calm_bonus + symbolic_resonance + lexical_focus + stability_bonus + mood_term
        decrease = drift_penalty + storm_penalty + 0.05  # decay

        self.value += increase
        self.value -= decrease

        # ------------------------------------------------------------
        # HOMEOSTATIC TARGET
        # ------------------------------------------------------------
        target = 0.3 + calm * 0.3 + stability * 0.3
        self.value += (target - self.value) * 0.06

        # ------------------------------------------------------------
        # SOFT SATURATION
        # ------------------------------------------------------------
        if self.value > 0.85:
            self.value -= (self.value - 0.85) * 0.5

        # ------------------------------------------------------------
        # CLAMP
        # ------------------------------------------------------------
        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        self.last_value = self.value
        return self.value
