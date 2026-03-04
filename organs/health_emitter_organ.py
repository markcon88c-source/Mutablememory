class HealthEmitterOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.state = {
            "hp": 100,
            "max_hp": 100,
            "fatigue": 0.0,
            "wounds": [],
            "regen": 0.01
        }

    def tick(self, heartbeat=None, packet=None):
        self.state["hp"] = min(
            self.state["max_hp"],
            self.state["hp"] + self.state["regen"]
        )

        self.creature.bus.emit(
            source="health_emitter",
            channel="health",
            kind="vital_state",
            payload=self.state
        )
