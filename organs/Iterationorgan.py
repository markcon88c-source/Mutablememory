# ============================================================
#  ITERATION ORGAN v1
#  - Performs 1–8 refinement passes
#  - Smooths, tightens, and finalizes the sentence
# ============================================================

import random

class IterationOrgan:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Compute iteration count (1–8 breaths)
    # --------------------------------------------------------
    def compute_iterations(self, drift, stability, pressure, chaos, clarity):
        # More turbulence → more breaths needed
        turbulence = drift + chaos

        # More stability/clarity → fewer breaths needed
        coherence = stability + clarity

        # Base iterations
        base = 4

        # Adjust
        iterations = base + int((turbulence - coherence) * 0.5)

        # Clamp to 1–8
        return max(1, min(8, iterations))

    # --------------------------------------------------------
    # One refinement pass
    # --------------------------------------------------------
    def refine_once(self, words, blocks, drift, stability, pressure, echo, chaos, clarity):
        refined = words[:]

        # Remove extremely low-energy words
        if random.random() < 0.3:
            low_energy = sorted(blocks, key=lambda b: b.forces.magnitude())
            if low_energy:
                w = low_energy[0].word
                if w in refined and len(refined) > 3:
                    refined.remove(w)

        # Reinforce high-clarity words
        if random.random() < 0.3:
            high_clarity = sorted(blocks, key=lambda b: b.forces.clarity, reverse=True)
            if high_clarity:
                refined.append(high_clarity[0].word)

        # Smooth transitions by sorting by energy
        if random.random() < 0.4:
            refined.sort(key=lambda w: self._energy_of(w, blocks))

        # Reduce chaos by pushing chaotic words to the end
        if chaos > 2.5:
            refined.sort(key=lambda w: self._chaos_of(w, blocks))

        # Pressure expansion
        if pressure > 3.0:
            mids = [b.word for b in blocks if not b.ascended]
            if mids and random.random() < 0.3:
                refined.append(random.choice(mids))

        return refined

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    def _energy_of(self, word, blocks):
        for b in blocks:
            if b.word == word:
                return b.forces.magnitude()
        return 0.0

    def _chaos_of(self, word, blocks):
        for b in blocks:
            if b.word == word:
                return b.forces.chaos
        return 0.0

    # --------------------------------------------------------
    # Main entry
    # --------------------------------------------------------
    def process(self, words, blocks, drift, stability, pressure, echo, chaos, clarity):
        iterations = self.compute_iterations(drift, stability, pressure, chaos, clarity)
        refined = words[:]

        for _ in range(iterations):
            refined = self.refine_once(refined, blocks, drift, stability, pressure, echo, chaos, clarity)

        return {
            "words": refined,
            "iterations": iterations
        }
