# ============================================================
# VOCABULARY ORGAN — ECOLOGY LOADER + WORD EMITTER (1/heartbeat)
# ============================================================

import os
import random

class VocabularyOrgan:
    def __init__(self, creature):
        self.creature = creature

        # Three reservoirs
        self.identity_words = []   # names (mutable)
        self.faction_words = []    # factions (mutable)
        self.lexical_words = []    # verbs, nouns, descriptors, atmospherics

        # Load ecology files
        self.load_identity_ecology()
        self.load_faction_ecology()
        self.load_core_vocabulary()

    # --------------------------------------------------------
    # Load character identity ecology
    # --------------------------------------------------------
    def load_identity_ecology(self):
        path = "organs/Identity_Ecology_Character.txt"
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                cols = line.split()
                if len(cols) == 0:
                    continue

                identity = cols[0]
                self.add_word(identity, "identity")

                for w in cols[1:]:
                    self.add_word(w, "lexical")

    # --------------------------------------------------------
    # Load faction ecology
    # --------------------------------------------------------
    def load_faction_ecology(self):
        path = "organs/Identity_Ecology_Faction.txt"
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                cols = line.split()
                if len(cols) == 0:
                    continue

                faction = cols[0]
                self.add_word(faction, "faction")

                for w in cols[1:]:
                    self.add_word(w, "lexical")

    # --------------------------------------------------------
    # Load core vocabulary reservoir (core.txt)
    # --------------------------------------------------------
    def load_core_vocabulary(self):
        path = "vocabulary/reservoirs/core/core.txt"
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if not word or word.startswith("#"):
                    continue
                self.add_word(word, "lexical")

    # --------------------------------------------------------
    # Add word to correct reservoir
    # --------------------------------------------------------
    def add_word(self, word, wclass):
        if not word:
            return

        if wclass == "identity":
            if word not in self.identity_words:
                self.identity_words.append(word)

        elif wclass == "faction":
            if word not in self.faction_words:
                self.faction_words.append(word)

        else:
            if word not in self.lexical_words:
                self.lexical_words.append(word)

    # --------------------------------------------------------
    # Packet receiver — mutation + ingestion
    # --------------------------------------------------------
    def receive(self, packet):
        if not isinstance(packet, dict):
            return

        ptype = packet.get("type")
        payload = packet.get("payload", {})

        # Metabolic spark
        if ptype == "vocabulary_seed":
            tokens = payload.get("tokens", [])
            for t in tokens:
                self.add_word(t, "lexical")
            return

        # Legacy mutation packets
        word = payload.get("word")
        wclass = payload.get("class")

        if ptype == "identity_word":
            self.add_word(word, "identity")
            return

        if ptype == "faction_word":
            self.add_word(word, "faction")
            return

        if ptype == "lexical_word":
            self.add_word(word, "lexical")
            return

    # --------------------------------------------------------
    # Outward-facing vocabulary
    # --------------------------------------------------------
    def get_all_words(self):
        return (
            self.identity_words +
            self.faction_words +
            self.lexical_words
        )

    # --------------------------------------------------------
    # Modern tick — emits MeaningOrgan‑compatible lexical packets
    # --------------------------------------------------------
    def tick(self):
        if not self.lexical_words:
            return None

        word = random.choice(self.lexical_words)

        bus = getattr(self.creature, "bus", None)
        if bus is not None:
            bus.emit({
                "type": "lexical",
                "channel": "lexical",
                "source": "vocabulary",
                "kind": "lexical_word",
                "lexical": {
                    "word": word
                }
            })

        # Also return the vocabulary frame (legacy compatibility)
        frame = {
            "type": "vocabulary_frame",
            "identity": list(self.identity_words),
            "factions": list(self.faction_words),
            "lexical": list(self.lexical_words)
        }

        return {"vocabulary": frame}
