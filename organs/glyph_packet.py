# ============================================================
#  GLYPH PACKET ORGAN – v1.0 (Support‑Safe MathBlock Edition)
#  Expands a single glyph into a complex internal structure:
#    - vector signature
#    - shape identity
#    - resonance field
#    - complexity coefficient
#    - echo pattern
#    - subglyph generation
#    - symbolic signature
# ============================================================

import random
import math
from organs.glyph_mapper import GlyphMapper


class GlyphPacket:
    @staticmethod
    def build(glyph, forces):
        """
        Build a complex mathblock-like packet from:
          - glyph (A–Z + Ø)
          - forces (spark, drift, echo, chaos, clarity, memory, pressure)
        Always safe, always returns a full packet.
        """

        # ----------------------------------------------------
        # 1. Base vector (force-modulated)
        # ----------------------------------------------------
        vector = [
            forces["spark"] * random.uniform(0.8, 1.2),
            forces["drift"] * random.uniform(0.8, 1.2),
            forces["echo"] * random.uniform(0.8, 1.2),
            forces["chaos"] * random.uniform(0.8, 1.2),
            forces["clarity"] * random.uniform(0.8, 1.2),
            forces["memory"] * random.uniform(0.8, 1.2),
            forces["pressure"] * random.uniform(0.8, 1.2),
        ]

        # ----------------------------------------------------
        # 2. Shape identity (derived from glyph index)
        # ----------------------------------------------------
        index = GlyphMapper.glyph_to_index(glyph)
        shapes = ["point", "line", "arc", "triad", "cluster", "ring", "coil"]
        shape = shapes[index % len(shapes)]

        # ----------------------------------------------------
        # 3. Resonance field (force-weighted)
        # ----------------------------------------------------
        resonance = (
            forces["spark"] * 0.3 +
            forces["echo"] * 0.4 +
            forces["clarity"] * 0.3
        )

        # ----------------------------------------------------
        # 4. Complexity coefficient
        # ----------------------------------------------------
        complexity = (
            forces["chaos"] * 0.6 +
            forces["memory"] * 0.4 +
            random.uniform(0.05, 0.15)
        )

        # ----------------------------------------------------
        # 5. Echo pattern (mini-vector)
        # ----------------------------------------------------
        echo_pattern = [
            forces["echo"],
            (forces["echo"] + forces["memory"]) / 2,
            max(0.0, forces["echo"] - forces["drift"])
        ]

        # ----------------------------------------------------
        # 6. Subglyph generation (chaos-driven)
        # ----------------------------------------------------
        subglyphs = []
        if forces["chaos"] > 0.4:
            count = 1 if forces["chaos"] < 0.7 else 2
            for _ in range(count):
                subglyphs.append(
                    GlyphMapper.ALPHABET[random.randint(0, 26)]
                )

        # ----------------------------------------------------
        # 7. Symbolic signature
        # ----------------------------------------------------
        signature = f"{glyph}:{''.join(subglyphs)}:{complexity:.2f}"

        # ----------------------------------------------------
        # 8. Final packet
        # ----------------------------------------------------
        return {
            "glyph": glyph,
            "vector": vector,
            "shape": shape,
            "resonance": resonance,
            "complexity": complexity,
            "echo_pattern": echo_pattern,
            "subglyphs": subglyphs,
            "signature": signature,
        }
