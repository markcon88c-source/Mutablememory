# ============================================================
#  CLARITY ORGAN v1
#  - Restores coherence after chaos
#  - Uses clarity force, memory, inverse chaos, inverse drift
#  - Smooths transitions and prepares for Iteration
# ============================================================

import math

class ClarityOrgan:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Compute clarity score
    # --------------------------------------------------------
    def compute_clarity(self, blocks, chaos, drift, pressure):
        if not blocks:
            return 0.0

        # Base clarity from blocks
        clarity_force = sum(b.forces.clarity for b in blocks)

        # Memory stabilizes meaning
        memory_force = sum(b.forces.memory for b in blocks)

        # Chaos reduces clarity
        chaos_penalty = chaos * 0.6

        # Drift reduces clarity (energy differences)
        drift_penalty = drift * 0.4

        # Pressure distorts clarity if too high
        pressure_penalty = max(0.0, pressure - 2.0) * 0.5

        clarity_score = (
            clarity_force +
            memory_force -
            chaos_penalty -
            drift_penalty -
            pressure_penalty
        )

        return clarity_score

    # --------------------------------------------------------
    # Adjust sentence based on clarity
    # --------------------------------------------------------
    def adjust_sentence(self, words, blocks, clarity_score):
        adjusted = words[:]

        # High clarity → sort by clarity force
        if clarity_score > 3.0:
            adjusted.sort(key=lambda w: self._clarity_of(w, blocks), reverse=True)

        # Medium clarity → sort by memory force
        elif clarity_score > 1.0:
            adjusted.sort(key=lambda w: self._memory_of(w, blocks), reverse=True)

        # Low clarity → push chaotic words to the end
        else:
            adjusted.sort(key=lambda w: self._chaos_of(w, blocks))

        return adjusted

    # --------------------------------------------------------
    # Helpers to read block forces by word
    # --------------------------------------------------------
    def _clarity_of(self, word, blocks):
        for b in blocks:
            if b.word == word:
                return b.forces.clarity
        return 0.0

    def _memory_of(self, word, blocks):
        for b in blocks:
            if b.word == word:
                return b.forces.memory
        return 0.0

    def _chaos_of(self, word, blocks):
        for b in blocks:
            if b.word == word:
                return b.forces.chaos
        return 0.0

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------
    def process(self, words, blocks, chaos, drift, pressure):
        clarity_score = self.compute_clarity(blocks, chaos, drift, pressure)
        adjusted_words = self.adjust_sentence(words, blocks, clarity_score)

        return {
            "words": adjusted_words,
            "clarity": clarity_score
        }
