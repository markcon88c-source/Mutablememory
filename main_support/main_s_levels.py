# main_support/main_s_levels.py
# S-Levels sandbox with:
# - worldbuilding flow
# - reservoir flow
# - 12-word rotating sample
# - viewer-friendly output

import time
import random
import sys
import os

# ensure organs/ is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from organs.s_levels_organ import SLevelsOrgan
from organs.s_levels_viewer import SLevelsViewer


class SLevelsMain:
    def __init__(self):
        self.slevels = SLevelsOrgan()
        self.viewer = SLevelsViewer()

        self.tick = 0

        # ---------------------------------------------------------
        # WORLD-BUILDING FLOW (handcrafted)
        # ---------------------------------------------------------
        self.worldbuilding_words = [
            ("ember", "mythic"),
            ("veil", "dream"),
            ("fracture", "action"),
            ("echo", "mystery"),
            ("memory", "drama"),
            ("path", "epic"),
            ("hollow", "horror"),
            ("glyph", "mythic"),
            ("tide", "dream"),
            ("shard", "action"),
        ]

        # ---------------------------------------------------------
        # RESERVOIR FLOW (loaded from file)
        # ---------------------------------------------------------
        reservoir_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "vocabulary",
            "reservoir.txt"
        )

        self.reservoir_words = []

        if os.path.exists(reservoir_path):
            with open(reservoir_path, "r") as f:
                for line in f:
                    w = line.strip()
                    if w:
                        self.reservoir_words.append((w, "drama"))

        # ---------------------------------------------------------
        # SAMPLING SYSTEM (12-word rotating sample)
        # ---------------------------------------------------------
        self.sample_size = 12
        self.sample_refresh_rate = 30   # refresh every 30 ticks
        self.reservoir_sample = []

        # ---------------------------------------------------------
        # FLOW SWITCHES
        # ---------------------------------------------------------
        self.use_worldbuilding = True
        self.use_reservoir = True

    # -------------------------------------------------------------
    # WORD SELECTION LOGIC
    # -------------------------------------------------------------
    def _choose_word(self):
        """Choose a word from worldbuilding + a SAMPLE of the reservoir."""

        # refresh reservoir sample periodically
        if self.tick % self.sample_refresh_rate == 0:
            if self.reservoir_words:
                self.reservoir_sample = random.sample(
                    self.reservoir_words,
                    min(self.sample_size, len(self.reservoir_words))
                )

        choices = []

        # worldbuilding flow
        if self.use_worldbuilding:
            choices.extend(self.worldbuilding_words)

        # reservoir sample flow
        if self.use_reservoir and self.reservoir_sample:
            # weighted so sample doesn't drown worldbuilding
            choices.extend(random.choices(self.reservoir_sample, k=3))

        if not choices:
            return ("ember", "mythic")

        return random.choice(choices)

    # -------------------------------------------------------------
    # MAIN STEP
    # -------------------------------------------------------------
    def step(self):
        self.tick += 1

        word, stype = self._choose_word()

        event = {
            "word": word,
            "story_type": stype,
            "glyph": "?"
        }

        s_state = self.slevels.step_from_event(event)
        self.viewer.step(s_state)

    # -------------------------------------------------------------
    # RUN LOOP
    # -------------------------------------------------------------
    def run(self):
        while True:
#            print("🔮 S-Levels Tick")
            self.step()
            time.sleep(0.5)


def main():
    SLevelsMain().run()


if __name__ == "__main__":
    main()
