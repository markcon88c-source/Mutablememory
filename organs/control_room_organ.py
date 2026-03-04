class ControlRoomOrgan:
    """
    The Control Room is the arbiter of the emotional system.
    It reads all pressures + mood and applies balancing forces:
    - dampens runaway storms
    - prevents alert spirals
    - boosts calm when instability rises
    - boosts word strength when clarity is needed
    - prevents stagnation by injecting small variation
    """

    def __init__(self):
        self.last_state = {
            "storm": 0.0,
            "alert": 0.0,
            "calm": 0.0,
            "symbolic": 0.0,
            "concentration": 0.0,
            "word_strength": 0.0,
        }

    def compute(self, state):
        p = state["pressures"]
        mood = state["mood"]
        drift = state["drift"]["intensity"]

        storm = p["storm"]
        alert = p["alert"]
        calm = p["calm"]
        symbolic = p["symbolic"]
        concentration = p["concentration"]
        word_strength = p["word_strength"]

        valence = mood["valence"]
        arousal = mood["arousal"]
        stability = mood["stability"]

        # -----------------------------------------
        # 1. Detect stagnation (no movement)
        # -----------------------------------------
        stagnation = 0.0
        for key in self.last_state:
            stagnation += abs(p[key] - self.last_state[key])
        stagnation = 1.0 - min(1.0, stagnation * 2.0)

        # -----------------------------------------
        # 2. Balancing forces
        # -----------------------------------------
        corrections = {}

        # Storm too high → push down
        corrections["storm"] = -0.25 * storm * (1.0 - stability)

        # Alert too high → push down
        corrections["alert"] = -0.20 * alert * (1.0 - calm)

        # Calm too low during instability → push up
        drift_instability = abs(drift - self.last_state["storm"])
        corrections["calm"] = 0.20 * drift_instability + 0.15 * (1.0 - stability)

        # Word strength too low → push up
        corrections["word_strength"] = 0.20 * concentration + 0.10 * valence

        # Symbolic overload → push down slightly
        corrections["symbolic"] = -0.10 * symbolic * arousal

        # NEW: ensure concentration is always included
        corrections["concentration"] = 0.0

        # -----------------------------------------
        # 3. Anti‑stagnation nudge
        # -----------------------------------------
        nudge = 0.05 * (1.0 - stability)
        for key in corrections:
            corrections[key] += nudge

        # -----------------------------------------
        # 4. Apply corrections
        # -----------------------------------------
        adjusted = {}
        for key in corrections:
            raw = p[key] + corrections[key]
            adjusted[key] = max(0.0, min(1.0, round(raw, 3)))

        # -----------------------------------------
        # 5. Save last state
        # -----------------------------------------
        for key in self.last_state:
            self.last_state[key] = p[key]

        return adjusted




