from organs.base_organ import BaseOrgan
from organs.base_packet_source import BasePacketSource
import random

class WorldIdeaOrgan(BaseOrgan, BasePacketSource):
    """
    Generates world-idea packets: mutated names, proto-factions, proto-species,
    myth-seeds, and conceptual atoms for worldbuilding.

    This organ is upstream of WorldOrgan, StoryOrgan, SymbolicOrgan,
    ShadowCycleOrgan, and PressureOrgan. It feeds them raw conceptual matter.
    """

    def __init__(self, creature):
        # Cathedral-grade constructor: always accept creature and pass it upward
        super().__init__(creature)
        self.name = "WorldIdeaOrgan"

        # phoneme clusters for mutation
        self.phonemes = [
            "ar", "ur", "ir", "al", "ul", "fl", "ra", "la", "ia", "ah",
            "in", "un", "on", "os", "is", "ae", "ua", "ru", "fa"
        ]

        # conceptual tags that attach to mutated names
        self.concepts = [
            "tribe", "sect", "order", "clan", "species", "beast",
            "myth", "cult", "region", "spirit", "element", "faction"
        ]

    # ------------------------------------------------------------
    # Core mutation engine
    # ------------------------------------------------------------
    def mutate_name(self, base):
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

        # mutate by replacing one chunk
        if chunks:
            idx = random.randint(0, len(chunks)-1)
            chunks[idx] = random.choice(self.phonemes)

        mutated = "".join(chunks).capitalize()

        # add a soft ending sometimes
        if random.random() < 0.4:
            mutated += random.choice(["h", "n", "s", "in", "ah", "un"])

        return mutated

    # ------------------------------------------------------------
    # Idea packet generator
    # ------------------------------------------------------------
    def generate_idea_packet(self, base_name):
        mutated = self.mutate_name(base_name)
        tag = random.choice(self.concepts)

        return {
            "type": "world_idea",
            "base": base_name,
            "mutated": mutated,
            "concept": tag,
            "seed": f"{mutated} as a {tag}"
        }

    # ------------------------------------------------------------
    # Bus emission
    # ------------------------------------------------------------
    def heartbeat(self, creature):
        if not hasattr(creature, "world_seeds"):
            return

        for seed in creature.world_seeds:
            packet = self.generate_idea_packet(seed)
            self.emit(packet)
