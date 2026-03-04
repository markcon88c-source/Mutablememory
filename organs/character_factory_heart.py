# organs/character_factory_heart.py
# HEART-BASED CHARACTER FACTORY
# This is the new identity engine.
# It replaces the old CharacterFactory system entirely.

from organs.heart_character import HeartCharacter


class HeartCharacterFactory:
    """
    Builds unified HeartCharacters directly from the NameHeart packet.
    The old CharacterFactory (mythic/proto) system is no longer used.
    """

    def __init__(self, creature):
        self.creature = creature

    def create(self):
        # 1. Pull the latest NameHeart packet
        packet = self.creature.last_heart_packet
        if packet is None:
            return None

        # 2. Build unified HeartCharacter directly from the packet
        return HeartCharacter(packet)
