from dataclasses import dataclass

@dataclass
class StructureForceEngine:
    story_modifiers: dict

    def compute_force_values(self, blocks, verb, obj, modifier, word_data):
        """
        Compute structure forces using MathBlocks + minimal structure.
        """

        # basic force extraction from blocks
        spark = sum(b.force for b in blocks) / max(len(blocks), 1)
        drift = spark * 0.8
        echo = spark * 0.6
        chaos = spark * 0.4
        clarity = spark * 0.5
        memory = spark * 0.7
        pressure = spark * 0.9

        # if we have verb/object/modifier, add simple interactions
        if verb and obj and obj in word_data:
            # clusters placeholder
            clusters = word_data[obj].get("clusters", {})
            clarity += clusters.get(verb, 0) * 0.2

        return {
            "spark": spark,
            "drift": drift,
            "echo": echo,
            "chaos": chaos,
            "clarity": clarity,
            "memory": memory,
            "pressure": pressure
        }

    # ---------------------------------------------------------
    # STABILITY COMPUTATION
    # ---------------------------------------------------------
    def compute_stability(self, forces):
        """
        Compute a simple stability score from structure forces.
        Stability is the inverse of chaos and drift, and the
        reinforcement of clarity and memory.
        """

        if not forces:
            return 0.0

        chaos = forces.get("chaos", 0)
        drift = forces.get("drift", 0)
        clarity = forces.get("clarity", 0)
        memory = forces.get("memory", 0)

        stability = (clarity + memory) - (chaos + drift)

        # clamp to [-1, 1]
        if stability > 1:
            stability = 1
        if stability < -1:
            stability = -1

        return stability
