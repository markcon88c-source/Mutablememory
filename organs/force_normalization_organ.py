# organs/force_normalization_organ.py
# Modernized, pressure-aware force normalization organ
# Safe drop-in replacement

class ForceNormalizationOrgan:
    def __init__(self, creature=None):
        self.creature = creature

    def compute_force(self, normalized):
        """
        Compute force using modernized, pressure-aware physics.
        """

        spark = normalized.get("spark", 0.0)
        clarity = normalized.get("clarity", 0.0)
        memory = normalized.get("memory", 0.0)
        chaos = normalized.get("chaos", 0.0)
        storm = normalized.get("storm", 0.0)

        # --- Base force calculation (legacy physics) ---
        fs = (
            spark * 0.35 +
            clarity * 0.30 +
            memory * 0.20 -
            chaos * 0.25 +
            storm * 0.10
        )

        # ------------------------------------------------
        # MODERNIZATION LAYER
        # ------------------------------------------------

        creature = self.creature

        # 1. Gentle global damping (prevents constant 1.00 spikes)
        fs *= 0.75

        # 2. Calm pressure softens force
        if creature and hasattr(creature, "calm_pressure"):
            fs *= (0.90 + (creature.calm_pressure.value * 0.10))

        # 3. Chaos pressure reduces force slightly
        if creature and hasattr(creature, "chaos_pressure"):
            fs *= (1.00 - (creature.chaos_pressure.value * 0.15))

        # 4. Symbolic pressure stabilizes force
        if creature and hasattr(creature, "symbolic_pressure"):
            fs += (creature.symbolic_pressure.value * 0.05)

        # 5. Clamp to safe range
        fs = max(0.0, min(1.0, fs))

        return fs

    def normalize_packet(self, packet):
        """
        Normalize a single packet's force values.
        """

        if "forces" not in packet:
            return packet

        normalized = packet["forces"]

        # Compute modern force score
        packet["force_score"] = self.compute_force(normalized)

        return packet

    def normalize(self, packets):
        """
        Normalize all packets in a list.
        """

        if not packets:
            return packets

        return [self.normalize_packet(p) for p in packets]
