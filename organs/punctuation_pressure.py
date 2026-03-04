class PunctuationPressure:
    """
    Governs punctuation tendencies based on internal forces.
    Not yet hooked into STM or L-level, but ready for it.
    """

    def __init__(self, creature):
        self.creature = creature

        # Core punctuation set — expandable
        self.punctuations = [
            ".",   # period
            ",",   # comma
            "?",   # question
            "!",   # exclamation
            "…",   # ellipsis
            "—",   # em dash
            "\n",  # newline
            "    " # indent (4 spaces)
        ]

        # Pressure values (0–1) — these will be shaped by forces
        self.pressure = {
            ".": 0.0,
            ",": 0.0,
            "?": 0.0,
            "!": 0.0,
            "…": 0.0,
            "—": 0.0,
            "\n": 0.0,
            "    ": 0.0
        }

    # ---------------------------------------------------------
    # 1. Update punctuation pressure based on internal forces
    # ---------------------------------------------------------
    def update(self):
        mood = self.creature.mood.state
        drift = self.creature.pressure_core.drift
        focus = self.creature.pressure_core.focus
        pause = self.creature.pressure_core.pause

        # Baseline pressure (tiny hum)
        base = 0.01

        # Mood-driven tendencies
        self.pressure["."] = base + focus * 0.4 + pause * 0.2
        self.pressure[","] = base + drift * 0.5
        self.pressure["?"] = base + mood["curious"] * 0.6
        self.pressure["!"] = base + mood["alert"] * 0.7
        self.pressure["…"] = base + drift * 0.3 + pause * 0.3
        self.pressure["—"] = base + drift * 0.2 + focus * 0.2
        self.pressure["\n"] = base + pause * 0.5
        self.pressure["    "] = base + pause * 0.7  # indent

        # Normalize to 0–1
        max_val = max(self.pressure.values()) or 1
        for k in self.pressure:
            self.pressure[k] /= max_val

    # ---------------------------------------------------------
    # 2. Hesitation curve (4 orders of magnitude)
    # ---------------------------------------------------------
    def hesitation(self, value):
        """
        Applies a 4th-power hesitation curve.
        Small pressures stay tiny.
        Large pressures explode.
        """
        return value ** 4

    # ---------------------------------------------------------
    # 3. Choose punctuation based on pressure + hesitation
    # ---------------------------------------------------------
    def choose(self):
        weighted = []
        for p, val in self.pressure.items():
            w = self.hesitation(val)
            weighted.append((p, w))

        total = sum(w for _, w in weighted) or 1
        puncts = [p for p, _ in weighted]
        weights = [w / total for _, w in weighted]

        import random
        return random.choices(puncts, weights=weights, k=1)[0]

    # ---------------------------------------------------------
    # 4. Placeholder for STM influence (not active yet)
    # ---------------------------------------------------------
    def apply_stm_bias(self):
        """
        Future hook:
        STM words will bias punctuation tendencies.
        Not implemented yet.
        """
        pass

    # ---------------------------------------------------------
    # 5. Placeholder for L-level influence (not active yet)
    # ---------------------------------------------------------
    def apply_llevel_bias(self):
        """
        Future hook:
        L-level memory will shape punctuation habits.
        Not implemented yet.
        """
        pass
