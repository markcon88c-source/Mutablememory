from organs.base_organ import BaseOrgan
from organs.base_packet_source import BasePacketSource
import random

class NameHeartOrgan(BaseOrgan, BasePacketSource):
    """
    Generates character-name idea packets: mutated names, proto-lineages,
    heroic/villainous variants, and identity seeds for characters.

    This organ is upstream of SymbolicOrgan, StoryOrgan, ReasonOrgan,
    and MemoryOrgan. It feeds them raw identity matter.
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
    # Core name mutation
    # ------------------------------------------------------------
    def mutate_name(self, base):
        """
        Takes a name like 'Elar' and mutates it into:
        - Alen
        - Elair
        - Arlen
        - Miren
        - etc.
        """
        base = base.lower()

        # break into rough syllables
        chunks = []
        i = 0
        while i < len(base):
            if i < len(base) - 1 and base[i:i+2] in self.phonemes:
                chunks.append(base[i:i+2])
                i += 2
            else:
                chunks.append(base[i])
                i += 1

        # mutate one chunk
        if chunks:
            idx = random.randint(0, len(chunks)-1)
            chunks[idx] = random.choice(self.phonemes)

        mutated = "".join(chunks).capitalize()

        # optional soft ending
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
    # Bus emission
    # ------------------------------------------------------------
    def heartbeat(self, creature):
        if not hasattr(creature, "name_seeds"):
            return

        for seed in creature.name_seeds:
            packet = self.generate_name_packet(seed)
            self.emit(packet)
