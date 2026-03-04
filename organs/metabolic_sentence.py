# ============================================================
#  METABOLIC SENTENCE ORGAN v1
#  - Activates after ascension succeeds
#  - Builds full sentence from ascended + mid-band words
#  - Runs 8-breath metabolic refinement
# ============================================================

import random

class MetabolicSentenceOrgan:

    def __init__(self, letter_forces):
        self.LETTER_FORCES = letter_forces

    # --------------------------------------------------------
    # Compute sentence force (sum of word forces)
    # --------------------------------------------------------
    def compute_sentence_force(self, blocks):
        total = {
            "spark": 0.0,
            "drift": 0.0,
            "echo": 0.0,
            "chaos": 0.0,
            "clarity": 0.0,
            "memory": 0.0,
            "pressure": 0.0,
        }

        for b in blocks:
            f = b.forces.as_dict()
            for k in total:
                total[k] += f[k]

        return total

    # --------------------------------------------------------
    # Build initial sentence skeleton
    # --------------------------------------------------------
    def build_skeleton(self, ascended_blocks, mid_blocks):
        # Ascended words are anchors
        anchors = [b.word for b in ascended_blocks]

        # Pull 1–3 mid-band words to support them
        support = random.sample(mid_blocks, k=min(len(mid_blocks), random.randint(1,3)))

        support_words = [b.word for b in support]

        # Simple skeleton: anchors first, then support
        return anchors + support_words, ascended_blocks + support

    # --------------------------------------------------------
    # Metabolic refinement (8 breaths)
    # --------------------------------------------------------
    def refine_sentence(self, words, blocks, identity, memory, world):
        # 8 metabolic breaths
        for _ in range(8):
            # Drift: reorder words slightly
            if random.random() < 0.4:
                random.shuffle(words)

            # Echo: repeat an ascended word
            if random.random() < 0.2:
                asc = [b.word for b in blocks if b.ascended]
                if asc:
                    words.append(random.choice(asc))

            # Chaos: remove a random word
            if random.random() < 0.15 and len(words) > 2:
                words.pop(random.randrange(len(words)))

            # Pressure: add a mid-band stabilizer
            if random.random() < 0.25:
                mids = [b.word for b in blocks if not b.ascended]
                if mids:
                    words.append(random.choice(mids))

        return words

    # --------------------------------------------------------
    # Main entry: build final sentence
    # --------------------------------------------------------
    def build_sentence(self, ascended, mid, identity, memory, world):
        if not ascended:
            return {
                "sentence": "",
                "force": None,
                "words": [],
                "blocks": []
            }

        # 1. Build skeleton
        words, blocks = self.build_skeleton(ascended, mid)

        # 2. Refine across metabolic breaths
        final_words = self.refine_sentence(words, blocks, identity, memory, world)

        # 3. Compute final sentence force
        sentence_force = self.compute_sentence_force(blocks)

        # 4. Join into final sentence
        sentence = " ".join(final_words)

        return {
            "sentence": sentence,
            "force": sentence_force,
            "words": final_words,
            "blocks": blocks
        }
