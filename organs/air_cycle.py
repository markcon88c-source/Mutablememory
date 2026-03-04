class AirCycleOrgan:
    """
    Cathedral-era Air Cycle Organ.
    Governs the math-block atmosphere:
      - turbulence
      - lift
      - conceptual weather
      - pressure gradients
      - symbolic inhibition & crystallization
    """

    def __init__(self, creature):
        self.creature = creature
        self.pressure = 0.0
        self.turbulence = 0.0
        self.lift = 0.0

    def _f(self, x, default=0.0):
        try:
            return float(x)
        except:
            return default

    def compute(self, state):
        p = state.get("pressures", {}) or {}

        calm = self._f(p.get("calm"))
        storm = self._f(p.get("storm"))
        symbolic = self._f(p.get("symbolic"))
        drift = self._f(state.get("drift"))
        stability = self._f(state.get("stability"))
        crystallization = self._f(p.get("conceptual_crystallization"))
        inhibition = self._f(p.get("semantic_inhibition"))

        # -----------------------------
        # Atmospheric pressure
        # -----------------------------
        self.pressure = (
            calm * 0.3 +
            stability * 0.3 +
            symbolic * 0.2 -
            storm * 0.2
        )

        # Clamp
        self.pressure = max(0.0, min(1.0, self.pressure))

        # -----------------------------
        # Turbulence (air storms)
        # -----------------------------
        drift_mid = 1.0 - abs(drift - 0.5) * 2.0
        self.turbulence = (
            storm * 0.5 +
            inhibition * 0.3 +
            (1.0 - stability) * 0.2 +
            drift_mid * 0.2
        )

        self.turbulence = max(0.0, min(1.0, self.turbulence))

        # -----------------------------
        # Lift (math-block rising force)
        # -----------------------------
        self.lift = (
            symbolic * 0.4 +
            crystallization * 0.3 +
            calm * 0.2 -
            storm * 0.2
        )

        self.lift = max(0.0, min(1.0, self.lift))

        # -----------------------------
        # Write to state
        # -----------------------------
        state["air_pressure"] = self.pressure
        state["air_turbulence"] = self.turbulence
        state["air_lift"] = self.lift

        self.creature._last_state = state
        return state
