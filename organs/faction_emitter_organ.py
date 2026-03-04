class FactionEmitterOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.current_faction = None

    def set_faction(self, faction_dict):
        self.current_faction = faction_dict

    def tick(self, heartbeat=None, packet=None):
        if not self.current_faction:
            return

        self.creature.bus.emit(
            source="faction_emitter",
            channel="faction",
            kind="faction_state",
            payload=self.current_faction
        )
