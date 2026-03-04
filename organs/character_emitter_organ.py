class CharacterEmitterOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.current_identity = None

    def set_identity(self, identity_dict):
        self.current_identity = identity_dict

    def tick(self, heartbeat=None, packet=None):
        if not self.current_identity:
            return

        self.creature.bus.emit(
            source="character_emitter",
            channel="character",
            kind="mutated_identity",
            payload=self.current_identity
        )
