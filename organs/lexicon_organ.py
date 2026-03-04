# organs/lexicon_organ.py

import random

class LexiconOrgan:
    """
    Reservoir / vocabulary organ.
    Emits ONE reservoir word per heartbeat.
    Provides choose_word() for English_Field compatibility.
    """

    def __init__(self, packet_bus, path="vocabulary/reservoirs/core/core.txt"):
        self.packet_bus = packet_bus
        self.words = []

        # Load reservoir words
        try:
            with open(path, "r") as f:
                for line in f:
                    w = line.strip()
                    if w and not w.startswith("#"):
                        self.words.append(w)
        except Exception as e:
            print("LexiconOrgan: failed to load reservoir:", e)

        # Fallback if reservoir empty
        if not self.words:
            self.words = ["begin"]

    # ------------------------------------------------------------
    # HEARTBEAT EMISSION
    # ------------------------------------------------------------
    def step(self):
        """
        Emit ONE reservoir word per heartbeat.
        Returns a list of packets (for injector compatibility).
        """
        word = random.choice(self.words)
        return [{
            "type": "reservoir_word",
            "word": word
        }]

    # ------------------------------------------------------------
    # ENGLISH_FIELD COMPATIBILITY
    # ------------------------------------------------------------
    def choose_word(self):
        """
        English_Field calls this during brushup metabolism.
        Returns a single reservoir word.
        """
        if not self.words:
            return ""
        return random.choice(self.words)
