class AlertPressure:
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

        storm = self._to_float(pressures.get("storm", 0.0), 0.0)
        symbolic = self._to_float(pressures.get("symbolic", 0.0), 0.0)
        concentration = self._to_float(pressures.get("concentration", 0.0), 0.0)
        calm = self._to_float(pressures.get("calm", 0.0), 0.0)

        stm = state.get("STM", {})
        if not isinstance(stm, dict):
            stm = {}

        L1 = stm.get("L1", [])
        L2 = stm.get("L2", [])
        L3 = stm.get("L3", [])
        if not isinstance(L1, list):
            L1 = []
        if not isinstance(L2, list):
            L2 = []
        if not isinstance(L3, list):
            L3 = []

        # Baseline vigilance
        baseline = 0.05

        # Drift spikes
        drift_delta = abs(drift - self._to_float(self.last_drift, 0.0))
        self.last_drift = drift
        drift_spike = drift_delta * 0.30

        # Storm and symbolic overload
        storm_factor = storm * 0.20
        symbolic_factor = symbolic * 0.10

        # Low concentration raises alert
        concentration_penalty = (1.0 - concentration) * 0.20

        # Empty STM raises alert
        stm_empty = 0.0
        if len(L1) == 0 and len(L2) == 0 and len(L3) == 0:
            stm_empty = 0.15

        # Calm reduces alert
        calm_soothing = calm * 0.30

        increase = baseline + drift_spike + storm_factor + symbolic_factor + concentration_penalty + stm_empty
        decrease = 0.06 + calm_soothing  # natural decay + calm

        self.value += increase
        self.value -= decrease

        # Gentle pull toward mid‑range (prevents sticking at 1 or 0)
        target = 0.3
        self.value += (target - self.value) * 0.05

        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        return self.value