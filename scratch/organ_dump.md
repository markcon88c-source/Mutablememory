# ============================================================
# LEXICAL ORGAN — Cathedral v10 (token-native)
# ============================================================

import os
import random
from organs.base_organ import BaseOrgan

# ------------------------------------------------------------
# Simple phoneme decomposition
# ------------------------------------------------------------

PHONEME_MAP = {
    "a": ["æ"], "e": ["ɛ"], "i": ["i"], "o": ["ɔ"], "u": ["ʊ"],
    "y": ["j"], "r": ["ɹ"], "l": ["l"], "m": ["m"], "n": ["n"],
    "s": ["s"], "t": ["t"], "k": ["k"], "p": ["p"], "b": ["b"],
    "f": ["f"], "v": ["v"], "h": ["h"], "g": ["g"], "d": ["d"],
}

def word_to_phonemes(word):
    out = []
    for ch in word.lower():
        if ch in PHONEME_MAP:
            out.extend(PHONEME_MAP[ch])
    return out

# ------------------------------------------------------------
# Phoneme categories + base forces + reservoir bias
# ------------------------------------------------------------

PHONEME_CATEGORY = {
    "æ": "vowel", "ɛ": "vowel", "i": "vowel", "ɔ": "vowel", "ʊ": "vowel",
    "j": "approximant", "ɹ": "approximant",
    "l": "liquid",
    "m": "nasal", "n": "nasal",
    "s": "fricative", "f": "fricative", "v": "fricative", "h": "fricative",
    "t": "plosive", "k": "plosive", "p": "plosive", "b": "plosive",
    "g": "plosive", "d": "plosive",
}

PHONEME_FORCE_BASE = {
    "vowel":       {"spark": 0.15, "drift": 0.15, "echo": 0.80, "gravity": 0.25},
    "plosive":     {"spark": 0.90, "drift": 0.25, "echo": 0.15, "gravity": 0.35},
    "fricative":   {"spark": 0.35, "drift": 0.80, "echo": 0.25, "gravity": 0.20},
    "liquid":      {"spark": 0.25, "drift": 0.35, "echo": 0.55, "gravity": 0.80},
    "approximant": {"spark": 0.45, "drift": 0.45, "echo": 0.45, "gravity": 0.45},
    "nasal":       {"spark": 0.20, "drift": 0.40, "echo": 0.50, "gravity": 0.60},
}

RESERVOIR_FORCE_BIAS = {
    "proto":     {"spark": +0.20, "drift": +0.20, "echo": +0.10},
    "function":  {"gravity": +0.20, "echo": -0.05},
    "noun/adj":  {"gravity": +0.25, "echo": +0.15},
    "verb":      {"spark": +0.30, "drift": +0.15},
    "core":      {"gravity": +0.40, "echo": +0.20},
    "character": {"spark": +0.50, "gravity": +0.50, "echo": +0.30},
}

def _clamp01(x):
    return max(0.0, min(1.0, x))

def categorize_phoneme(p):
    return PHONEME_CATEGORY.get(p, "vowel")

# ============================================================
# LEXICAL ORGAN — v10 TOKEN NATIVE
# ============================================================

class LexicalOrgan(BaseOrgan):
    def __init__(self, creature, vocabulary):
        super().__init__(creature)
        self.vocabulary = vocabulary
        self.token_space = creature.token_space

        # Load core.txt
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            core_path = os.path.join(base, "..", "vocabulary", "reservoirs", "core", "core.txt")
            core_path = os.path.abspath(core_path)
            with open(core_path, "r") as f:
                for line in f:
                    w = line.strip()
                    if w and not w.startswith("#"):
                        token = self.token_space.normalize(w)
                        self.vocabulary.tokens.add(token)
            print(f"[lexical/v10] loaded core.txt → {len(self.vocabulary.tokens)} tokens")
        except Exception as e:
            print("[lexical/v10] failed to load core.txt:", e)

        # Load structural vocabulary
        self.structure_words = []
        try:
            struct_path = os.path.join(base, "..", "vocabulary", "reservoirs", "core", "CoreStructure.txt")
            struct_path = os.path.abspath(struct_path)
            with open(struct_path, "r") as f:
                for line in f:
                    w = line.strip()
                    if w and not w.startswith("#"):
                        self.structure_words.append(w)
            print(f"[lexical/v10] loaded CoreStructure.txt → {len(self.structure_words)} structural tokens")
        except Exception as e:
            print("[lexical/v10] failed to load CoreStructure.txt:", e)

        self.vocabulary.mass = len(self.vocabulary.tokens)
        self.vocabulary.gravity = min(1.0, self.vocabulary.mass / 20.0)

        # Wells
        self.proto_words = vocabulary.proto_words
        self.function_words = vocabulary.function_words
        self.noun_words = vocabulary.noun_words
        self.adj_words = vocabulary.adj_words
        self.verb_words = vocabulary.verb_words

        # Character reservoir
        self.character_source = None

        self.last_word = ""

    # --------------------------------------------------------
    # RESERVOIR SELECTOR
    # --------------------------------------------------------
    def choose_well(self, ignition):
        if ignition < 0.30:
            return self.proto_words, "proto"
        if ignition < 0.60:
            return self.function_words, "function"
        if ignition < 0.90:
            combined = self.noun_words + self.adj_words
            return combined, "noun/adj"
        if ignition < 0.97:
            return self.verb_words, "verb"
        if self.character_source:
            chars = self.character_source()
            if chars:
                return chars, "character"
        return list(self.vocabulary.tokens), "core"

    # --------------------------------------------------------
    # BUILD PHONEME FORCES
    # --------------------------------------------------------
    def build_phoneme_forces(self, phonemes, well_name, ignition, stability):
        last_gravity = float(getattr(self.creature, "last_gravity", 0.0))
        last_delta = float(getattr(self.creature.recursion, "last_delta", 0.0))
        recur_stability = float(getattr(self.creature.recursion, "stability", 0.0))

        base_energy = _clamp01(len(phonemes) / 8.0)
        forces = []

        for p in phonemes:
            category = categorize_phoneme(p)
            base = dict(PHONEME_FORCE_BASE.get(category, PHONEME_FORCE_BASE["vowel"]))

            # Reservoir bias
            bias = RESERVOIR_FORCE_BIAS.get(well_name, {})
            for k, v in bias.items():
                base[k] = _clamp01(base.get(k, 0.0) + v)

            # Ignition modulation
            for k in ("spark", "drift", "echo", "gravity"):
                base[k] = _clamp01(base[k] * (0.7 + 0.6 * ignition))

            # Delta modulation
            base["drift"] = _clamp01(base["drift"] * (0.7 + 0.8 * last_delta))
            base["spark"] = _clamp01(base["spark"] * (0.7 + 0.5 * last_delta))

            # Gravity modulation
            base["gravity"] = _clamp01(base["gravity"] * (0.7 + 0.8 * last_gravity))

            # Turbulence modulation
            turbulence = _clamp01(1.0 - recur_stability)
            base["echo"] = _clamp01(base["echo"] * (0.7 + 0.5 * turbulence))

            # Energy modulation
            for k in ("spark", "drift", "echo", "gravity"):
                base[k] = _clamp01(base[k] * (0.6 + 0.8 * base_energy))

            forces.append(base)

        return forces

    # --------------------------------------------------------
    # TICK — choose words and emit lexical + proto tokens
    # --------------------------------------------------------
    def tick(self):
        ignition = getattr(self.creature, "ignition_level", 0.0)
        stability = getattr(self.creature.recursion, "stability", 0.0)

        well, well_name = self.choose_well(ignition)
        if not well:
            return

        # BREATH-BASED WORD INTAKE
        last_stability = getattr(self.creature.recursion, "last_stability", stability)
        is_rising = stability > last_stability
        self.creature.recursion.last_stability = stability

        if stability > 2.0 and is_rising:
            intake_mode = "structural"
        elif stability < 2.0 and not is_rising:
            intake_mode = "chaotic"
        else:
            intake_mode = "frozen"

        # Apply intake mode
        if intake_mode == "structural":
            word = random.choice(self.structure_words) if self.structure_words else random.choice(well)
        elif intake_mode == "chaotic":
            word = random.choice(self.proto_words) if self.proto_words else random.choice(well)
        else:  # frozen
            word = self.last_word or random.choice(well)

        self.last_word = word

        # TOKENIZE
        token = self.token_space.normalize(word)

        # PHONEMES + FORCES
        phonemes = word_to_phonemes(word)
        forces = self.build_phoneme_forces(phonemes, well_name, ignition, stability)

        # MAIN lexical emission (token-native)
        self.bus.emit({
            "type": "lexical",
            "token": token,
            "well": well_name,
            "ignition": ignition,
            "stability": stability,
            "phonemes": phonemes,
            "phoneme_forces": forces,
            "source": "lexical",
        })

        # Proto-sentence emission (token-native)
        self.bus.emit({
            "type": "proto_sentence",
            "proto_tokens": [token],
            "well": well_name,
            "ignition": ignition,
            "stability": stability,
            "source": "lexical",
        })

        # SECONDARY lexical emission
        word2 = random.choice(well)
        if stability > 0.5:
            try:
                idx2 = well.index(word)
                idx2 = max(0, min(len(well) - 1, idx2 + random.choice([-1, 1])))
                word2 = well[idx2]
            except ValueError:
                pass

        token2 = self.token_space.normalize(word2)
        phonemes2 = word_to_phonemes(word2)
        forces2 = self.build_phoneme_forces(phonemes2, well_name, ignition, stability)

        self.bus.emit({
            "type": "lexical",
            "token": token2,
            "well": well_name,
            "ignition": ignition,
            "stability": stability,
            "phonemes": phonemes2,
            "phoneme_forces": forces2,
            "source": "lexical",
        })

        self.bus.emit({
            "type": "proto_sentence",
            "proto_tokens": [token2],
            "well": well_name,
            "ignition": ignition,
            "stability": stability,
            "source": "lexical",
        })

    def receive(self, packet):
        return

