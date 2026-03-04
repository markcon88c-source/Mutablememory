# organs/iteration_organ.py
# ============================================================
# ITERATION ORGAN — performs 8-breath force-driven refinement
# and logs expressive emoji events to the IterationViewer.
# ============================================================

import random

class IterationOrgan:
    def __init__(self, creature):
        self.creature = creature

    def refine(self, words, meta):

        # 8-breath improvement cycle
        for breath in range(8):

            spark   = meta.get("spark", 0.0)
            drift   = meta.get("drift", 0.0)
            chaos   = meta.get("chaos", 0.0)
            clarity = meta.get("clarity", 0.0)

            improvement_pressure = chaos + spark - clarity

            mutated = False
            added_word = None
            pruned_word = None

            if improvement_pressure > 0:

                add_bias = spark - drift

                if add_bias > 0:
                    new_word = self.creature.vocabulary_organ.choose_word()
                    if new_word:
                        words.append(new_word)
                        added_word = new_word
                        mutated = True
                else:
                    if len(words) > 1:
                        pruned = random.choice(words)
                        words.remove(pruned)
                        pruned_word = pruned
                        mutated = True

            # expressive emoji logging
            emoji = self.creature.iteration_viewer._breath_emoji(
                spark, drift, chaos, clarity,
                mutated, added_word, pruned_word
            )

            self.creature.iteration_viewer.breath_log.append(emoji)

        return words
