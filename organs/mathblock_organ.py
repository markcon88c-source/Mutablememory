# ============================================================
#  MATHBLOCK ORGAN v2 — Hybrid Resonance Engine
#  - Keeps original MathBlock + ForceVector dataclasses
#  - Adds resonance vectors for identity selection
#  - Provides word/sentence/character/faction mathblocks
#  - Fully compatible with SentenceBuilderOrgan
# ============================================================

from dataclasses import dataclass, field
from typing import Dict, List, Any
import math
import random

# ------------------------------------------------------------
# Force Vector (7 forces) — preserved
# ------------------------------------------------------------

@dataclass
class ForceVector:
    spark: float = 0.0
    drift: float = 0.0
    echo: float = 0.0
    chaos: float = 0.0
    clarity: float = 0.0
    memory: float = 0.0
    pressure: float = 0.0

    def as_dict(self):
        return {
            "spark": self.spark,
            "drift": self.drift,
            "echo": self.echo,
            "chaos": self.chaos,
            "clarity": self.clarity,
            "memory": self.memory,
            "pressure": self.pressure,
        }

    def magnitude(self):
        d = self.as_dict()
        return math.sqrt(sum(v*v for v in d.values()))

# ------------------------------------------------------------
# MathBlock structure — preserved
# ------------------------------------------------------------

@dataclass
class MathBlock:
    word: str
    core: float
    shell: Dict[str, Any]
    semantic_vector: List[float]
    forces: ForceVector
    level: int = 1
    micro_gate: int = 0
    ascended: bool = False
    canon: bool = False

# ============================================================
# MATHBLOCK ORGAN v2 — Hybrid Resonance Engine
# ============================================================

class MathBlockOrgan:

    def __init__(self, creature):
        self.creature = creature

        # Registries for fast lookup
        self.word_vectors: Dict[str, List[float]] = {}
        self.sentence_vectors: Dict[str, List[float]] = {}
        self.character_vectors: Dict[str, List[float]] = {}
        self.faction_vectors: Dict[str, List[float]] = {}

        # Keep original symbolic blocks if needed
        self.symbolic_blocks: Dict[str, MathBlock] = {}

    # --------------------------------------------------------
    # Utility: normalized vector
    # --------------------------------------------------------
    def normalize(self, vec):
        mag = math.sqrt(sum(x*x for x in vec))
        if mag == 0:
            return vec
        return [x / mag for x in vec]

    # --------------------------------------------------------
    # Utility: deterministic vector from string
    # --------------------------------------------------------
    def vector_from_string(self, s):
        seed = sum(ord(c) for c in s)
        rnd = random.Random(seed)
        vec = [rnd.uniform(-1.0, 1.0) for _ in range(8)]
        return self.normalize(vec)

    # --------------------------------------------------------
    # WORD MATHBLOCK (resonance vector)
    # --------------------------------------------------------
    def get_word_mathblock(self, word):
        if not word:
            return [0.0] * 8

        if word not in self.word_vectors:
            self.word_vectors[word] = self.vector_from_string(word)

        return self.word_vectors[word]

    # --------------------------------------------------------
    # SENTENCE MATHBLOCK (combined vector)
    # --------------------------------------------------------
    def get_sentence_mathblock(self, text):
        if not text:
            return [0.0] * 8

        if text in self.sentence_vectors:
            return self.sentence_vectors[text]

        words = text.split()
        accum = [0.0] * 8

        for w in words:
            wv = self.get_word_mathblock(w)
            for i in range(8):
                accum[i] += wv[i]

        vec = self.normalize(accum)
        self.sentence_vectors[text] = vec
        return vec

    # --------------------------------------------------------
    # CHARACTER MATHBLOCKS (identity reservoir)
    # --------------------------------------------------------
    def get_character_mathblocks(self):
        vocab = getattr(self.creature, "vocabulary", None)
        if not vocab:
            return {}

        out = {}
        for name in vocab.identity_words:
            if name not in self.character_vectors:
                self.character_vectors[name] = self.vector_from_string(name)
            out[name] = self.character_vectors[name]

        return out

    # --------------------------------------------------------
    # FACTION MATHBLOCKS (faction reservoir)
    # --------------------------------------------------------
    def get_faction_mathblocks(self):
        vocab = getattr(self.creature, "vocabulary", None)
        if not vocab:
            return {}

        out = {}
        for name in vocab.faction_words:
            if name not in self.faction_vectors:
                self.faction_vectors[name] = self.vector_from_string(name)
            out[name] = self.faction_vectors[name]

        return out

    # --------------------------------------------------------
    # OPTIONAL: Build symbolic MathBlock (preserved)
    # --------------------------------------------------------
    def build_symbolic_block(self, word):
        # Placeholder symbolic block using minimal fields
        forces = ForceVector()
        core = forces.magnitude()
        shell = {c: [] for c in word.upper()}
        semantic_vector = [0.0] * 27

        block = MathBlock(
            word=word,
            core=core,
            shell=shell,
            semantic_vector=semantic_vector,
            forces=forces
        )

        self.symbolic_blocks[word] = block
        return block
