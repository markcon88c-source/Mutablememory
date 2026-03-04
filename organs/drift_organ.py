import random

class DriftOrgan:
    """
    DriftOrgan computes drift from energy differences between blocks
    and optionally adjusts sentence word order based on drift magnitude.
    This version preserves your physiology exactly, only fixing structure.
    """

    def __init__(self, bus):
        self.bus = bus

    # --------------------------------------------------------
    # Compute drift from energy differences
    # --------------------------------------------------------
    def compute_drift(self, blocks):
        energies = [b.forces.magnitude() for b in blocks]

        if not energies:
            return 0.0

        high = max(energies)
        low = min(energies)

        # Drift is the energy gradient
        drift = high - low

        return drift

    # --------------------------------------------------------
    # Adjust sentence based on drift
    # --------------------------------------------------------
    def adjust_sentence(self, words, drift):
        adjusted = words[:]

        # High drift → reorder aggressively
        if drift > 2.0:
            random.shuffle(adjusted)

        # Medium drift → swap two words
        elif drift > 1.0:
            if len(adjusted) > 2:
                i, j = random.sample(range(len(adjusted)), 2)
                adjusted[i], adjusted[j] = adjusted[j], adjusted[i]

        # Low drift → keep stable
        return adjusted

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------
    def process(self, words, blocks):
        drift = self.compute_drift(blocks)
        adjusted_words = self.adjust_sentence(words, drift)

        return {
            "words": adjusted_words,
            "drift": drift
        }
