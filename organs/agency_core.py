class AgencyCore:
    def __init__(self):
        self.stm = {}
        self.ltm = {}
        self.hooks = []
        self.output = ""

    def reset(self):
        self.stm = {}
        self.output = ""

    def load_memory(self, memory):
        if memory is None:
            return
        tone = memory.get("tone")
        if tone is not None:
            self.ltm["tone"] = tone

    def fire_hook(self, hook):
        if hook is None:
            return None
        self.hooks.append(hook)
        return hook

    def process_hook(self, hook):
        if hook is None:
            return None
        kind = hook.get("kind", "none")
        self.stm["tone"] = kind
        return {"tone": kind}

    def _update_ltm(self, memory):
        if memory is None:
            return
        tone = memory.get("tone", "none")
        if tone == "comfort":
            self.ltm["tone"] = "comfort"
        elif tone == "alert":
            self.ltm["tone"] = "alert"
        elif tone == "neutral":
            self.ltm["tone"] = "neutral"
        else:
            self.ltm["tone"] = "none"

    def drift(self):
        tone = self.ltm.get("tone", "neutral")
        if tone == "comfort":
            return "soft"
        if tone == "alert":
            return "sharp"
        if tone == "neutral":
            return "plain"
        return "flat"

    def generate_output(self):
        tone = self.stm.get("tone", "none")
        drift = self.drift()

        if tone == "comfort":
            self.output = "comfort + " + drift
        elif tone == "alert":
            self.output = "alert + " + drift
        elif tone == "neutral":
            self.output = "neutral + " + drift
        else:
            self.output = "default + " + drift

        return self.output

    def step(self, state, stm, hook, viewer, memory, english, drift_value):
        self.reset()

        fired = self.fire_hook(hook)
        memory_update = self.process_hook(fired)
        self._update_ltm(memory_update)

        output = self.generate_output()

        state = {
            "english": output,
            "tone": self.stm.get("tone", "none"),
            "drift": self.drift()
        }

        return state, self.stm
