# ============================================================
#  PRESSURE ORGAN v1
#  - Measures force density and developmental tension
#  - Expands or compresses the sentence
# ============================================================

import random
import math

class PressureOrgan:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Compute pressure score
    # --------------------------------------------------------
    def compute_pressure(self, blocks, stability):
        if not blocks:
            return 0.0

        # Total pressure from blocks
        block_pressure = sum(b.forces.pressure for b in blocks)

        # Force density = total pressure / number of words
        density = block_pressure / len(blocks)

        # Developmental tension = inverse stability
        tension = max(0.0, 2.0 - stability)

        # Final pressure score
        pressure = density + tension

        return pressure

    # --------------------------------------------------------
    # Adjust sentence based on pressure
    # --------------------------------------------------------
    def adjust_sentence(self, words, blocks, pressure):
        adjusted = words[:]

        # High pressure → expand sentence
        if pressure > 2.5:
            # Add 1–2 stabilizing words (if available)
            mids = [b.word for b in blocks if not b.ascended]
            if mids:
                for _ in range(random.randint(1,2)):
                    adjusted.append(random.choice(mids))

        # Medium pressure → keep as-is
        elif pressure > 1.0:
            pass

        # Low pressure → compress sentence
        else:
            if len(adjusted) > 3:
                adjusted = adjusted[:3]

        return adjusted

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------
    def process(self, words, blocks, stability):
        pressure = self.compute_pressure(blocks, stability)
        adjusted_words = self.adjust_sentence(words, blocks, pressure)

        return {
            "words": adjusted_words,
            "pressure": pressure
        }
