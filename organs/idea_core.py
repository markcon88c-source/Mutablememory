class IdeaCore:
    def __init__(self):
        self.idea = {
            "agent": None,
            "action": None,
            "quality": None,
            "relation": None
        }
        self.pressure = 0.0

    def reset(self):
        self.idea = {
            "agent": None,
            "action": None,
            "quality": None,
            "relation": None
        }
        self.pressure = 0.0

    def step(
        self,
        hook_word,
        comfort_word,
        shape,
        mood_state,
        drift
    ):
        calm = mood_state.get("calm", 0.0)
        curious = mood_state.get("curious", 0.0)
        bright = mood_state.get("bright", 0.0)
        alert = mood_state.get("alert", 0.0)

        base = (
            curious * 0.4 +
            bright * 0.3 +
            calm * 0.2
        )
        if alert > 0.7:
            base = base * 0.5
        if drift != "MY PATTERNS HELD":
            base = base * 0.5

        self.pressure = (
            0.7 * self.pressure +
            0.3 * base
        )

        filled_before = self._filled_slots()

        if shape and self.idea["agent"] is None:
            self.idea["agent"] = shape

        if hook_word and self.idea["action"] is None:
            self.idea["action"] = hook_word

        if comfort_word and self.idea["quality"] is None:
            self.idea["quality"] = comfort_word

        if (
            self.idea["relation"] is None and
            calm > 0.4
        ):
            self.idea["relation"] = "near"

        filled_after = self._filled_slots()

        if filled_after > filled_before:
            self.pressure = min(
                1.0,
                self.pressure + 0.1
            )
        else:
            self.pressure = max(
                0.0,
                self.pressure - 0.02
            )

        sentence = None
        if (
            self.idea["agent"] and
            self.idea["action"] and
            self.pressure > 0.5
        ):
            sentence = self._to_english()
            self.reset()

        return {
            "idea": self.idea,
            "pressure": self.pressure,
            "sentence": sentence
        }

    def _filled_slots(self):
        count = 0
        for k in self.idea:
            if self.idea[k] is not None:
                count += 1
        return count

    def _to_english(self):
        parts = []

        agent = self.idea["agent"]
        action = self.idea["action"]
        quality = self.idea["quality"]
        relation = self.idea["relation"]

        if agent:
            parts.append(agent)
        if action:
            parts.append("touches " + action)
        if quality:
            parts.append("with " + quality)
        if relation:
            parts.append(relation)

        text = " ".join(parts)
        text = text.strip()
        if len(text) == 0:
            text = "It drifts around an unnamed idea."
        text = text[0].upper() + text[1:]
        if not text.endswith("."):
            text = text + "."
        return text
