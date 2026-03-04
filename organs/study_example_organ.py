# organs/study_example_organ.py

import math

class StudyExampleOrgan:
    """
    Study Example Organ (Field-Based Version)

    - Holds example packs per story type.
    - Each example has: sentence, structure, forces.
    - Field-based similarity:
        * structure similarity
        * force similarity
        * modifier/tone similarity
        * word-shape similarity
    - color_if_example() highlights sentences that match the field,
      not the exact string.
    """

    def __init__(self):
        # Packs identical to before (not repeating here for brevity)
        # Use your existing packs exactly as they are.
        self.packs = {...}  # <-- keep your existing packs here

    # ---------------------------------------------------------
    # FORCE SIMILARITY
    # ---------------------------------------------------------
    def _force_similarity(self, f1, f2):
        keys = set(f1.keys()) & set(f2.keys())
        if not keys:
            return 0.0

        total = 0.0
        for k in keys:
            total += abs(f1[k] - f2[k])

        avg = total / len(keys)
        return max(0.0, min(1.0, 1.0 - avg))

    # ---------------------------------------------------------
    # STRUCTURE SIMILARITY
    # ---------------------------------------------------------
    def _structure_similarity(self, s1, s2):
        score = 0
        total = 4

        if s1["subject"] and s2["subject"]:
            if s1["subject"] == s2["subject"]:
                score += 1

        if s1["verb"] and s2["verb"]:
            if s1["verb"] == s2["verb"]:
                score += 1

        if s1["object"] and s2["object"]:
            if s1["object"] == s2["object"]:
                score += 1

        if s1["modifier"] and s2["modifier"]:
            if s1["modifier"] == s2["modifier"]:
                score += 1

        return score / total

    # ---------------------------------------------------------
    # WORD SHAPE SIMILARITY
    # ---------------------------------------------------------
    def _word_shape_similarity(self, sentence, example_sentence):
        s_words = set(sentence.lower().split())
        e_words = set(example_sentence.lower().split())

        if not s_words or not e_words:
            return 0.0

        overlap = len(s_words & e_words)
        union = len(s_words | e_words)

        return overlap / union

    # ---------------------------------------------------------
    # FIELD SIMILARITY (MAIN)
    # ---------------------------------------------------------
    def field_similarity(self, structure, forces, sentence):
        """
        Compare the critter's structure + forces + sentence
        to ALL examples across ALL packs.
        Return the highest similarity score found.
        """

        best = 0.0

        for story_type, examples in self.packs.items():
            for ex in examples:
                f_sim = self._force_similarity(forces, ex["forces"])
                s_sim = self._structure_similarity(structure, ex["structure"])
                w_sim = self._word_shape_similarity(sentence, ex["sentence"])

                # Weighted blend
                score = (f_sim * 0.5) + (s_sim * 0.3) + (w_sim * 0.2)

                if score > best:
                    best = score

        return best

    # ---------------------------------------------------------
    # COLORING
    # ---------------------------------------------------------
    def color_if_example(self, structure, forces, sentence):
        score = self.field_similarity(structure, forces, sentence)

        if score >= 0.75:
            return "\033[95m" + sentence + "\033[0m"  # magenta highlight
        return sentence
