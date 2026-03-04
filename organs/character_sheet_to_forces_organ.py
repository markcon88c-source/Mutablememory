# CHARACTER SHEET → FORCES ORGAN — CATHEDRAL DYNAMIC METABOLISM
# Converts character sheets into evolving force profiles based on:
# - Identity traits (stats, role, seed)
# - Current metabolic forces (spark, drift, pressure)
# - Narrative attractors (story packets)
# - Memory resonance (memory packets)
# - Chaos modulation (drift storms, pressure spikes)

from packets import character_forces_packet

class CharacterSheetToForcesOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.sheet = None
        self.story_bias = 0
        self.memory_resonance = 0
        self.chaos_seed = 1

    # Accept packets from upstream organs
    def accept(self, packet):
        ptype = packet.get("type")

        # Identity layer
        if ptype == "character_sheet":
            self.sheet = packet["payload"]

        # Narrative layer
        elif ptype == "story":
            self.story_bias += packet["payload"].get("emotional_weight", 0)

        # Memory layer
        elif ptype == "memory":
            self.memory_resonance += packet["payload"].get("echo", 0)

    # Dynamic metabolism — fires every tick
    def tick(self):
        if not self.sheet:
            return None

        # Identity traits
        stats = self.sheet.get("stats", {})
        role = self.sheet.get("role", "")
        seed = self.sheet.get("seed", "")

        # Current metabolic forces
        spark = self.creature.forces.get("spark", 1)
        drift = self.creature.forces.get("drift", 1)
        pressure = self.creature.forces.get("pressure", 1)

        # Chaotic modulation
        self.chaos_seed = (self.chaos_seed * 7 + drift + pressure) % 13
        chaos = (drift * pressure + self.story_bias + self.chaos_seed) % 9

        # Dynamic force synthesis
        forces = {
            "spark": stats.get("intelligence", 1) + spark + self.story_bias,
            "drift": stats.get("wisdom", 1) + drift + chaos,
            "pressure": stats.get("constitution", 1) + pressure,
            "memory": stats.get("history", 0) + self.memory_resonance,
            "chaos": chaos,
            "clarity": spark - drift + self.story_bias - chaos,
        }

        return character_forces_packet(forces)
