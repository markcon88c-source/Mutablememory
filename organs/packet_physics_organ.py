# organs/packet_physics_organ.py
# ============================================================
# 🧩 PACKET PHYSICS ORGAN — v7 (Hybrid Edition)
# ============================================================
# Responsibilities:
#  - Retrieve MathBlock for each word
#  - Expand MathBlock.force → full physics vector
#  - Modulate physics by MathBlock.category
#  - Return a complete physics dict for MeaningOrgan v7
# ============================================================

from typing import Dict, Any


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


class PacketPhysicsOrgan:
    def __init__(self, creature):
        self.creature = creature

    # ------------------------------------------------------------
    # MAIN ENTRYPOINT
    # ------------------------------------------------------------
    def compute(self, word: str) -> Dict[str, float]:
        """
        Expand MathBlock.force into a full physics vector.
        """

        block = self.creature.mathblocks.get_block(word)
        f = float(block.force)

        # --------------------------------------------------------
        # 1. BASE PHYSICS (viewer-era ratios)
        # --------------------------------------------------------
        spark = f
        chaos = f * 0.4
        storm = f * 0.3
        echo = f * 0.6
        gravity = f * 0.5
        symbolic = f * 0.2
        concentration = f * 0.3
        mood = f * 0.4

        # --------------------------------------------------------
        # 2. CATEGORY MODULATION (semantic physics)
        # --------------------------------------------------------
        cat = block.category.lower()

        if cat == "identity":
            # Identity words are anchors
            spark *= 1.2
            gravity *= 1.3
            chaos *= 0.7
            storm *= 0.7
            symbolic *= 1.1

        elif cat == "function":
            # Function words stabilize structure
            chaos *= 0.5
            storm *= 0.5
            concentration *= 1.2
            clarity_boost = f * 0.3
            spark += clarity_boost

        elif cat == "unknown":
            # Unknown words introduce chaos + storm
            chaos *= 1.4
            storm *= 1.4
            echo *= 0.9
            gravity *= 0.8
            mood *= 1.1

        # --------------------------------------------------------
        # 3. Clamp everything
        # --------------------------------------------------------
        return {
            "spark": _clamp(spark),
            "chaos": _clamp(chaos),
            "storm": _clamp(storm),
            "echo": _clamp(echo),
            "gravity": _clamp(gravity),
            "symbolic": _clamp(symbolic),
            "concentration": _clamp(concentration),
            "mood": _clamp(mood),
        }
