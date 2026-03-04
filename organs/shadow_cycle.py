class ShadowCycleOrgan:
    """
    Cathedral-era Air Cycle + Circadian Organ.
    Governs:
      - math-block atmosphere (pressure, turbulence, lift)
      - day/night metabolic cycle
      - circadian phase for ocean + meaning organs
    """

    def __init__(self, creature):
        self.creature = creature
        self.pressure = 0.0
        self.turbulence = 0.0
        self.lift = 0.0
        self.day_intensity = 0.0
        self.night_intensity = 0.0
        self.phase = 0.0

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
        depth = self._f(state.get("ocean_depth", 0.0))

        # Atmospheric pressure
        self.pressure = (
            calm * 0.3 +
            stability * 0.3 +
            symbolic * 0.2 -
            storm * 0.2
        )
        self.pressure = max(0.0, min(1.0, self.pressure))

        # Turbulence
        drift_mid = 1.0 - abs(drift - 0.5) * 2.0
        self.turbulence = (
            storm * 0.5 +
            inhibition * 0.3 +
            (1.0 - stability) * 0.2 +
            drift_mid * 0.2
        )
        self.turbulence = max(0.0, min(1.0, self.turbulence))

        # Lift
        self.lift = (
            symbolic * 0.4 +
            crystallization * 0.3 +
            calm * 0.2 -
            storm * 0.2
        )
        self.lift = max(0.0, min(1.0, self.lift))

        # -----------------------------
        # Circadian cycle
        # -----------------------------
        self.day_intensity = (
            symbolic * 0.35 +
            crystallization * 0.25 +
            stability * 0.25 +
            self.lift * 0.15
        )

        self.night_intensity = (
            storm * 0.35 +
            inhibition * 0.25 +
            depth * 0.20 +
            (1.0 - stability) * 0.20
        )

        # Phase: -1 (night) to +1 (day)
        self.phase = self.day_intensity - self.night_intensity

        state["day_intensity"] = self.day_intensity
        state["night_intensity"] = self.night_intensity
        state["circadian_phase"] = self.phase
        state["is_day"] = self.phase > 0
        state["is_night"] = self.phase < 0

        # Air outputs
        state["air_pressure"] = self.pressure
        state["air_turbulence"] = self.turbulence
        state["air_lift"] = self.lift

        self.creature._last_state = state
        return state
