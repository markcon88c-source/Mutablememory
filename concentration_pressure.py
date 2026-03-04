class ConcentrationPressure:
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

        raw_drift = state.get("drift", 0.0)
        drift = self._to_float(raw_drift, 0.0)

        alert = self._to_float(pressures.get("alert", 0.0), 0.0)
        symbolic = self._to_float(pressures.get("symbolic", 0.0), 0.0)
        storm = self._to_float(pressures.get("storm", 0.0), 0.0)
        calm = self._to_float(pressures.get("calm", 0.0), 0.0)

        # Drift stability helps focus
        drift_stability = max(0.0, 1.0 - abs(drift)) * 0.25

        # Drift instability hurts focus
        drift_delta = abs(drift - self._to_float(self.last_drift, 0.0))
        self.last_drift = drift
        drift_instability = drift_delta * 0.25

        # Alert and storm disrupt focus
        alert_penalty = alert * 0.35
        storm_penalty = storm * 0.20

        # Symbolic meaning slightly supports focus
        symbolic_factor = symbolic * 0.10

        # Calm slightly supports focus (can settle attention)
        calm_support = calm * 0.10

        increase = drift_stability + symbolic_factor + calm_support
        decrease = drift_instability + alert_penalty + storm_penalty + 0.05  # decay

        self.value += increase
        self.value -= decrease

        # Gentle pull toward mid‑range
        target = 0.4
        self.value += (target - self.value) * 0.05

        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        return self.value