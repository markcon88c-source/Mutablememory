class SymbolicPressure:
    def __init__(self):
        self.value = 0.0
        self.last_stm_depth = 0.0

    def _to_float(self, x, default=0.0):
        try:
            return float(x)
        except Exception:
            return default

    def compute(self, state):
        pressures = state.get("pressures", {})
        if not isinstance(pressures, dict):
            pressures = {}

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

        drift = self._to_float(state.get("drift", 0.0), 0.0)
        alert = self._to_float(pressures.get("alert", 0.0), 0.0)
        concentration = self._to_float(pressures.get("concentration", 0.0), 0.0)
        storm = self._to_float(pressures.get("storm", 0.0), 0.0)
        calm = self._to_float(pressures.get("calm", 0.0), 0.0)

        # STM depth as meaning load
        stm_depth = (
            len(L1) * 0.03 +
            len(L2) * 0.05 +
            len(L3) * 0.07
        )

        # Change in STM depth
        stm_delta = abs(stm_depth - self._to_float(self.last_stm_depth, 0.0))
        self.last_stm_depth = stm_depth
        stm_change = stm_delta * 0.20

        # Drift stability supports symbolic coherence
        drift_factor = max(0.0, 1.0 - abs(drift)) * 0.10

        # Concentration sharpens meaning
        concentration_factor = concentration * 0.15

        # Alert and storm suppress meaning
        alert_penalty = alert * 0.20
        storm_penalty = storm * 0.15

        # Calm can gently support symbolic integration
        calm_support = calm * 0.10

        increase = stm_depth + stm_change + drift_factor + concentration_factor + calm_support
        decrease = alert_penalty + storm_penalty + 0.06  # decay

        self.value += increase
        self.value -= decrease

        # Gentle pull toward mid‑range
        target = 0.5
        self.value += (target - self.value) * 0.04

        if self.value < 0.0:
            self.value = 0.0
        if self.value > 1.0:
            self.value = 1.0

        return self.value