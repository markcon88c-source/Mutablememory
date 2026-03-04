from organs.base_organ import BaseOrgan
from organs.base_packet_source import BasePacketSource
import random

class NameHeartOrgan(BaseOrgan, BasePacketSource):
    """
    Generates character-name idea packets: mutated names, proto-lineages,
    heroic/villainous variants, and identity seeds for characters.
    """

    def __init__(self):
        super().__init__()
        self.name = "NameHeartOrgan"

        # phoneme clusters for character names
        self.phonemes = [
            "el", "al", "ar", "an", "en", "ir", "il", "or", "ur",
            "la", "ra", "ka", "va", "sa", "tha", "rin", "len", "mir"
        ]

        # identity tags
        self.roles = [
            "hero", "villain", "wanderer", "seer", "warrior",
            "heir", "outcast", "guardian", "traitor", "prophet"
        ]

    # ------------------------------------------------------------
    # Modern Cathedral compatibility wrapper
    # ------------------------------------------------------------
    def tick(self, creature):
        return self.tick_legacy(creature)

    # ------------------------------------------------------------
    # Compatibility: old organs expect self.emit(packet)
    # ------------------------------------------------------------
    def emit(self, packet):
        if hasattr(self, "creature") and hasattr(self.creature, "bus"):
            self.creature.bus.emit(
                source="name_heart",
                channel="identity",
                kind="character_idea",
                payload=packet
            )

    # ------------------------------------------------------------
    # Core name mutation
    # ------------------------------------------------------------
    def mutate_name(self, base):
        base = base.lower()

        chunks = []
        i = 0
        while i < len(base):
            if i < len(base) - 1 and base[i:i+2] in self.phonemes:
                chunks.append(base[i:i+2])
                i += 2
            else:
                chunks.append(base[i])
                i += 1

        if chunks:
            idx = random.randint(0, len(chunks)-1)
            chunks[idx] = random.choice(self.phonemes)

        mutated = "".join(chunks).capitalize()

        if random.random() < 0.4:
            mutated += random.choice(["n", "r", "s", "el", "en", "ir"])

        return mutated

    # ------------------------------------------------------------
    # Packet generator
    # ------------------------------------------------------------
    def generate_name_packet(self, base_name):
        mutated = self.mutate_name(base_name)
        role = random.choice(self.roles)

        return {
            "type": "character_idea",
            "base": base_name,
            "mutated": mutated,
            "role": role,
            "seed": f"{mutated} as a {role}"
        }

    # ------------------------------------------------------------
    # Legacy heartbeat (renamed)
    # ------------------------------------------------------------
    def tick_legacy(self, creature):
        if not hasattr(creature, "name_seeds"):
            return

        for seed in creature.name_seeds:
            packet = self.generate_name_packet(seed)
            self.emit(packet)
