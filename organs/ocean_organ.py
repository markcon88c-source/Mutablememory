class OceanOrgan:
    """
    Cathedral-era Ocean Organ
    Drives the oceanic metabolism:
      - drifting sentence drops
      - depth, drift, strength, symbolic load
      - storm fronts, calm basins, symbolic tides
      - 10-pressure evolution
    """

    def __init__(self, creature):
        self.creature = creature
        self.drops = []  # each drop: {sentence, depth, drift, strength, symbolic}

    def _f(self, x, default=0.0):
        try:
            return float(x)
        except:
            return default

    # ---------------------------------------------------------
    # Create a new drop from a sentence
    # ---------------------------------------------------------
    def add_sentence(self, sentence, state):
        pressures = state.get("pressures", {}) or {}

        drop = {
            "sentence": sentence,
            "depth": 0.0,
            "drift": self._f(state.get("drift", 0.5)),
            "strength": self._f(pressures.get("word_strength", 0.5)),
            "symbolic": self._f(pressures.get("symbolic", 0.0)),
        }
        self.drops.append(drop)

    # ---------------------------------------------------------
    # Evolve a single drop using 10 pressures
    # ---------------------------------------------------------
    def evolve_drop(self, drop, state):
        p = state.get("pressures", {}) or {}

        calm = self._f(p.get("calm"))
        storm = self._f(p.get("storm"))
        symbolic = self._f(p.get("symbolic"))
        concentration = self._f(p.get("concentration"))
        alert = self._f(p.get("alert"))
        stability = self._f(state.get("stability"))
        drift = self._f(state.get("drift"))
        narrative = self._f(p.get("narrative_momentum"))
        coherence = self._f(p.get("coherence_binding"))
        crystallization = self._f(p.get("conceptual_crystallization"))

        # -----------------------------
        # Depth physics
        # -----------------------------
        depth_change = (
            calm * 0.05 +
            symbolic * 0.04 +
            concentration * 0.03 +
            narrative * 0.03 -
            storm * 0.06
        )
        drop["depth"] += depth_change

        # Clamp depth
        if drop["depth"] < 0.0:
            drop["depth"] = 0.0
        if drop["depth"] > 1.0:
            drop["depth"] = 1.0

        # -----------------------------
        # Drift physics
        # -----------------------------
        drift_pull = (
            stability * 0.04 -
            storm * 0.05 +
            coherence * 0.03
        )
        drop["drift"] += drift_pull

        # Clamp drift
        if drop["drift"] < 0.0:
            drop["drift"] = 0.0
        if drop["drift"] > 1.0:
            drop["drift"] = 1.0

        # -----------------------------
        # Strength physics
        # -----------------------------
        strength_change = (
            symbolic * 0.05 +
            crystallization * 0.05 +
            concentration * 0.04 -
            storm * 0.06
        )
        drop["strength"] += strength_change

        if drop["strength"] < 0.0:
            drop["strength"] = 0.0
        if drop["strength"] > 1.0:
            drop["strength"] = 1.0

        # -----------------------------
        # Symbolic load
        # -----------------------------
        drop["symbolic"] += (
            symbolic * 0.06 +
            coherence * 0.04 +
            narrative * 0.03 -
            storm * 0.05
        )

        if drop["symbolic"] < 0.0:
            drop["symbolic"] = 0.0
        if drop["symbolic"] > 1.0:
            drop["symbolic"] = 1.0

        return drop

    # ---------------------------------------------------------
    # Main step: evolve all drops and update state
    # ---------------------------------------------------------
    def step(self):
        state = getattr(self.creature, "_last_state", {}) or {}

        # If a new sentence arrived this cycle, add it
        new_sentence = state.get("new_sentence")
        if new_sentence:
            self.add_sentence(new_sentence, state)

        # Evolve all drops
        evolved = []
        for drop in self.drops:
            evolved.append(self.evolve_drop(drop, state))

        self.drops = evolved
        state["ocean"] = self.drops
        self.creature._last_state = state

        return self.drops
