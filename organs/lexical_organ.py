# ============================================================
# LEXICAL ORGAN — emits proto‑packets from VocabularyOrgan
# ============================================================

import random

class LexicalOrgan:
    def __init__(self, creature, vocabulary):
        self.creature = creature
        self.vocabulary = vocabulary   # pulls from core.txt + ecology

    # --------------------------------------------------------
    # Phonetic vector (lightweight, stable)
    # --------------------------------------------------------
    def phonetic_vector(self, word):
        return [(ord(c) % 32) / 32.0 for c in word.lower() if c.isalpha()]

    # --------------------------------------------------------
    # Proto‑force (primitive energy)
    # --------------------------------------------------------
    def proto_force(self, vec):
        if not vec:
            return 0.0
        return sum(vec) / len(vec)

    # --------------------------------------------------------
    # Cathedral heartbeat — emit proto‑packet
    # --------------------------------------------------------
    def tick(self):
        # Pull reservoir from VocabularyOrgan
        reservoir = self.vocabulary.lexical_words
        if not reservoir:
            return None

        # Choose a word from core.txt/ecology
        word = random.choice(reservoir)

        # Build proto‑fields
        phon = self.phonetic_vector(word)
        force = self.proto_force(phon)
        seed = word[:2].lower()

        # ====================================================
        # PROTO‑PACKET (MeaningOrgan‑compatible)
        # ====================================================
        proto = {
            "type": "lexical",
            "channel": "lexical",
            "source": "lexicon",
            "kind": "proto_word",

            # ---- Lexical layer (first nutrient) ----
            "lexical": {
                "word": word,
                "phonetic": phon,
                "force": force,
                "seed": seed,
                "words": [word],
                "phonetics": [phon],
            },

            # ---- Placeholders for later organs ----
            "identity": {},
            "faction": {},
            "forces": {},
            "emotion": {},
            "sentence": {},
            "story": {},
            "world": {},
        }

        # Emit into Cathedral bus
        bus = getattr(self.creature, "bus", None)
        if bus:
            bus.emit(packet=proto)

        return proto
