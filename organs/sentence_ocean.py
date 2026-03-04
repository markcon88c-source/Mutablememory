# organs/sentence_ocean.py
# Mythic, Stateful, Strength‑Scaled Ocean Organ (Drop‑Based Version)

class SentenceOceanOrgan:
    """
    The Ocean Organ is the creature’s subconscious tide engine.
    It stores a LIST of drops, each representing a transformed sentence.
    Each drop evolves over time with:
      - depth
      - strength
      - age
      - currents
      - symbolic drift
      - gremlin turbulence
    """

    def __init__(self, creature):
        self.creature = creature

        # Ocean is now a LIST of drops (viewer‑compatible)
        self.ocean = []

        # Internal state for tides, storms, symbolic depth, etc.
        self.state = {
            "tide": 0.0,
            "storm": 0.0,
            "gremlin": 0.0,
            "symbolic": 0.0,
            "undertow": 0.0,
            "last_strength": 0.0,
            "last_sentence": "",
            "mode": "calm",
        }

        # Currents summary for viewer
        self.currents = {
            "surface_strength": 0.0,
            "deep_strength": 0.0,
            "drift_strength": 0.0,
            "return_threshold": 0.15,
        }

    # ------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------

    def compute_strength(self, meta):
        """Compute a unified sentence strength score."""
        stability = meta.get("stability", 0.0)
        alert = meta.get("alert_pressure", {}).get("total", 0.0)
        drift = meta.get("drift_metrics", {}).get("drift", 0.0)
        symbolic = self.creature.pressures.get("symbolic", 0.0)

        strength = (
            stability * 0.55 +
            symbolic * 0.25 +
            drift * 0.15 -
            alert * 0.20
        )

        return max(0.0, min(1.0, strength))

    def update_state(self, strength, meta):
        """Update tides, storms, gremlins, symbolic depth, undertow with smoothing."""

        alert = meta.get("alert_pressure", {}).get("total", 0.0)
        drift = meta.get("drift_metrics", {}).get("drift", 0.0)
        symbolic = self.creature.pressures.get("symbolic", 0.0)
        gremlin = meta.get("alert_pressure", {}).get("sub_organs", {}).get("chaos_gremlin", 0.0)

        def smooth(old, new, factor=0.1):
            return old * (1 - factor) + new * factor

        self.state["tide"] = smooth(self.state["tide"], drift)
        self.state["storm"] = smooth(self.state["storm"], alert)
        self.state["symbolic"] = smooth(self.state["symbolic"], symbolic)
        self.state["gremlin"] = smooth(self.state["gremlin"], gremlin)

        undertow = meta.get("force_output", {}).get("force_values", {}).get("echo", 0.0)
        self.state["undertow"] = smooth(self.state["undertow"], abs(undertow))

        # MODE SELECTION
        prev_mode = self.state["mode"]

        if strength < 0.3:
            target = "calm"
        elif strength < 0.7:
            target = "hybrid"
        else:
            target = "mythic"

        if target != prev_mode:
            if abs(strength - self.state["last_strength"]) > 0.15:
                self.state["mode"] = target

        self.state["last_strength"] = strength

    # ------------------------------------------------------------
    # SENTENCE TRANSFORMATION
    # ------------------------------------------------------------

    def transform_sentence(self, sentence, strength):
        """Transform the sentence based on ocean state and strength."""
        words = sentence.split()
        mode = self.state["mode"]

        if mode == "calm":
            if len(words) > 1:
                words = sorted(words)
            return " ".join(words)

        if mode == "hybrid":
            if self.state["symbolic"] > 0.3:
                words.append("tide")
            if self.state["undertow"] > 0.3:
                words.insert(0, "softly")
            return " ".join(words)

        if mode == "mythic":
            if self.state["gremlin"] > 0.2:
                words.append("gremlin")
            if self.state["storm"] > 0.3:
                words.insert(0, "storm‑born")
            if self.state["tide"] > 0.3:
                words = words[::-1]
            return " ".join(words)

        return sentence

    # ------------------------------------------------------------
    # MAIN CYCLE — produces a DROP
    # ------------------------------------------------------------

    def cycle(self, packets):
        """
        Takes packets, transforms the sentence, updates state,
        and appends a new DROP to the ocean.
        """

        # Find the sentence packet
        sentence_packet = None
        for p in packets:
            if p.get("type") == "sentence":
                sentence_packet = p
                break

        if not sentence_packet:
            return None

        sentence = sentence_packet.get("sentence", "")
        meta = sentence_packet.get("meta", {})

        # Compute strength
        strength = self.compute_strength(meta)

        # Update ocean state
        self.update_state(strength, meta)

        # Transform sentence
        new_sentence = self.transform_sentence(sentence, strength)
        sentence_packet["sentence"] = new_sentence
        self.state["last_sentence"] = new_sentence

        # --------------------------------------------------------
        # CREATE DROP
        # --------------------------------------------------------
        drop = {
            "sentence": new_sentence,
            "strength": strength,
            "depth": self.state["tide"],
            "age": 0.0,
            "metadata": meta,
            "currents": {
                "tide": self.state["tide"],
                "storm": self.state["storm"],
                "symbolic": self.state["symbolic"],
                "undertow": self.state["undertow"],
                "gremlin": self.state["gremlin"],
            }
        }

        # Add drop to ocean
        self.ocean.append(drop)

        # Trim ocean size
        if len(self.ocean) > 200:
            self.ocean.pop(0)

        # Update currents summary for viewer
        self.currents["surface_strength"] = strength
        self.currents["deep_strength"] = self.state["undertow"]
        self.currents["drift_strength"] = self.state["tide"]

        # Route back to router
        return {
            "packets": packets,
            "meta": meta,
            "handoff": "language_viewer"
        }
