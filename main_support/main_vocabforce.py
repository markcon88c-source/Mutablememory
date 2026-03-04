# ============================================================
#  MAIN – VOCAB FORCE TEST HARNESS (Glyphic Edition)
#  Runs:
#    - HeartOrgan (symbolic glyph heartbeat)
#    - SentenceBuilder (glyph packets)
#    - SentenceViewer (glyph display)
# ============================================================

import os
import sys
import time

# ------------------------------------------------------------
# ENSURE PROJECT ROOT IS ON PATH (fixes ModuleNotFoundError)
# ------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------
from main_support.main_loader import load_creature
from organs.sentence_builder import SentenceBuilder
from organs.sentence_viewer import SentenceViewer


def run():
    print("\n=== VocabForce Test Harness (Glyphic Mode) ===\n")

    # Load creature
    creature = load_creature()

    # Attach glyphic organs (override old ones if present)
    creature.sentence_builder = SentenceBuilder(creature)
    creature.sentence_viewer = SentenceViewer(creature)

    # Main loop
    while True:
        # 1. Heart beat (symbolic glyph)
        creature.name_heart.beat()

        # 2. Generate glyphic sentence
        sentence = creature.sentence_builder.generate_sentence()

        # 3. Update viewer
        creature.sentence_viewer.update(sentence)

        # 4. Show viewer
        creature.sentence_viewer.show()

        # 5. Slow pacing
        time.sleep(1)


if __name__ == "__main__":
    run()

