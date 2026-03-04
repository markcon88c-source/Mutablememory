from packets import character_birth_packet

class CharacterBirthOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.has_fired = False

    def tick(self):
        if self.has_fired:
            return None

        birth = {
            "id": "creature-1",
            "name": getattr(self.creature, "name", "Unnamed"),
            "forces": {"spark": 1, "drift": 1, "pressure": 1},
            "seed": getattr(self.creature, "birth_seed", None),
        }

        self.has_fired = True
        return character_birth_packet(birth)
