class AmbientEmitterOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.mood = "neutral"
        self.pressure = 0.0

    def tick(self, heartbeat=None, packet=None):
        self.pressure += 0.01

        self.creature.bus.emit(
            source="ambient_emitter",
            channel="ambient",
            kind="environment_state",
            payload={
                "mood": self.mood,
                "pressure": self.pressure,
                "temperature": 22.0,
                "noise": 0.02
            }
        )
