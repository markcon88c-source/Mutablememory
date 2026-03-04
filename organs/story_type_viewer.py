# organs/story_type_viewer.py

import time
import os

class StoryTypeViewer:
    def __init__(self):
        # 20 STORY TYPES (your canonical set)
        self.story_types = [
            "drama",
            "tragedy",
            "comedy",
            "romance",
            "horror",
            "mystery",
            "adventure",
            "epic",
            "mythic",
            "dream",
            "surreal",
            "sci_fi",
            "fantasy",
            "chaos",
            "slice_of_life",
            "philosophical",
            "spiritual",
            "heroic",
            "melancholic",
            "cosmic",
        ]

        # Buckets store BOTH surface sentences and deep structures
        self.buckets = {t: [] for t in self.story_types}

        self.anim_speed = 0.03

    # ---------------------------------------------------------
    # CLASSIFICATION (placeholder — later force‑driven)
    # ---------------------------------------------------------
    def classify(self, sentence, structure=None):
        """
        Temporary classifier:
        - '?' pushes toward chaos
        - long subjects push toward mythic
        - verbs with motion push toward adventure
        - etc.
        """
        if "?" in sentence:
            return "chaos"

        if structure:
            subj = structure.get("subject", "")
            if len(subj) > 6:
                return "mythic"

        return "drama"  # default baseline story type

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------
    def store(self, sentence, structure, story_type):
        self.buckets[story_type].append({
            "sentence": sentence,
            "structure": structure,
        })

    # ---------------------------------------------------------
    # MAIN ENTRY POINT
    # ---------------------------------------------------------
    def process(self, sentence, structure):
        story_type = self.classify(sentence, structure)
        self._tube_animation(sentence, story_type)
        self.store(sentence, structure, story_type)
        return story_type

    # ---------------------------------------------------------
    # VISUAL: STORY TYPE TUBES
    # ---------------------------------------------------------
    def _tube_animation(self, sentence, target_type):
        os.system("clear")
        print(" 📚 STORY TYPE TUBES 📚")
        print("=" * 60)
        print(f"Incoming sentence:\n  \"{sentence}\"\n")
        print("Attempting to enter story tube...\n")

        for t in self.story_types:
            tube_label = t.upper().ljust(15)
            if t == target_type:
                print(f"{tube_label} | >>> {sentence}")
            else:
                print(f"{tube_label} |")
            time.sleep(self.anim_speed)

        print("\n✓ Stored in:", target_type.upper())
        time.sleep(0.6)


# ---------------------------------------------------------
# STANDALONE RUNNER (demo)
# ---------------------------------------------------------
if __name__ == "__main__":
    viewer = StoryTypeViewer()

    # Demo structure
    structure = {
        "subject": "river",
        "verb": "remembers",
        "object": "moon",
        "modifier": "softly",
    }

    # Demo sentence
    sentence = "river remembers moon softly."

    viewer.process(sentence, structure)
