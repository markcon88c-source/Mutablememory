# ============================================================
#  MATH BLOCK FORCE CORE – REWRITTEN GOVERNING ORGAN
#  - Surface word vs. internal glyphs (two languages)
#  - Letter-based 7-force alphabet
#  - Force-weighted glyph sampling (option C)
#  - 1–12 glyph MathBlocks, forces from glyphs
#  - Developmental ladder (11 x 17) + ascension
#  - Registry: one block per surface word
# ============================================================

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
import math
import random

# ------------------------------------------------------------
# FORCE NAMES
# ------------------------------------------------------------

FORCE_NAMES = [
    "spark",
    "drift",
    "echo",
    "chaos",
    "clarity",
    "memory",
    "pressure",
]

# ------------------------------------------------------------
# 7-FORCE VECTOR
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

    def as_dict(self) -> Dict[str, float]:
        return {name: getattr(self, name) for name in FORCE_NAMES}

    def magnitude(self) -> float:
        d = self.as_dict()
        return math.sqrt(sum(v * v for v in d.values()))

    def __add__(self, other: "ForceVector") -> "ForceVector":
        return ForceVector(
            spark=self.spark + other.spark,
            drift=self.drift + other.drift,
            echo=self.echo + other.echo,
            chaos=self.chaos + other.chaos,
            clarity=self.clarity + other.clarity,
            memory=self.memory + other.memory,
            pressure=self.pressure + other.pressure,
        )

# ------------------------------------------------------------
# MATH BLOCK
# ------------------------------------------------------------

@dataclass
class MathBlock:
    # Surface identity
    word: str
    id: int

    # Internal MathBlock identity (underneath language)
    glyphs: str  # 1–12 glyphs

    # Structure
    core: float
    shell: Dict[str, List[int]] = field(default_factory=dict)
    semantic_vector: List[float] = field(default_factory=list)

    # Forces (from glyphs)
    forces: ForceVector = field(default_factory=ForceVector)

    # Developmental ladder
    level: int = 1
    micro_gate: int = 0
    ascended: bool = False
    canon: bool = False

    # Flow flag for wiring / viewers
    flow_flag: bool = False

# ------------------------------------------------------------
# GOVERNING MATH BLOCK FORCE CORE
# ------------------------------------------------------------

class MathBlockForceCore:
    """
    Governing organ for all MathBlocks.

    Two-language model:
      - Surface word language (meaning, arbitrary length)
      - MathBlock glyph language (1–12 glyphs, force atoms)

    Responsibilities:
      - Maintain letter → 7-force alphabet
      - Build MathBlocks via force-weighted glyph sampling
      - Compute forces from glyphs
      - Run developmental ladder + ascension
      - Maintain registry (one block per surface word)
      - Provide viewer-friendly snapshots
    """

    LEVELS = 11
    GATES = 17

    def __init__(self):
        # Letter-force alphabet
        self.ALPHABET, self.LETTER_FORCES = self._build_letter_force_alphabet()

        # Development thresholds
        self.thresholds = self._build_thresholds()

        # Registry
        self.blocks_by_word: Dict[str, MathBlock] = {}
        self.next_id: int = 1

    # --------------------------------------------------------
    # LETTER-FORCE ALPHABET
    # --------------------------------------------------------
    def _build_letter_force_alphabet(self) -> Tuple[str, Dict[str, ForceVector]]:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        forces: Dict[str, ForceVector] = {}
        for ch in alphabet:
            forces[ch] = ForceVector(
                spark=random.random(),
                drift=random.random(),
                echo=random.random(),
                chaos=random.random(),
                clarity=random.random(),
                memory=random.random(),
                pressure=random.random(),
            )
        return alphabet, forces

    # --------------------------------------------------------
    # LEVEL THRESHOLDS
    # --------------------------------------------------------
    def _build_thresholds(self) -> Dict[int, Dict[str, float]]:
        out: Dict[int, Dict[str, float]] = {}
        for lvl in range(1, self.LEVELS + 1):
            base = 0.08 * lvl
            out[lvl] = {
                "spark": base,
                "drift": 0.03 * lvl,
                "echo": base,
                "chaos": 0.02 * lvl,
                "clarity": base,
                "memory": base,
                "pressure": base + 0.04 * lvl,
            }
        return out

    # --------------------------------------------------------
    # PUBLIC API – REGISTRY
    # --------------------------------------------------------
    def get_or_create_block_for_word(self, word: str) -> MathBlock:
        """
        Main entry: returns the canonical MathBlock for a surface word.
        Builds it (word + glyphs) if it does not exist yet.
        """
        if word not in self.blocks_by_word:
            block = self._build_block_from_word(word)
            self.blocks_by_word[word] = block
        return self.blocks_by_word[word]

    def all_blocks(self) -> List[MathBlock]:
        return list(self.blocks_by_word.values())

    # --------------------------------------------------------
    # WORD → RAW FORCE SIGNATURE (MEANING SHAPE)
    # --------------------------------------------------------
    def _sanitize_word(self, word: str) -> str:
        clean = ''.join(ch for ch in word if ch.isalpha()).upper()
        return clean

    def _compute_raw_word_force(self, word: str) -> ForceVector:
        """
        Raw force signature from the surface word's letters.
        Used only to shape glyph sampling probabilities.
        """
        clean = self._sanitize_word(word)
        f = ForceVector()
        for ch in clean:
            if ch in self.LETTER_FORCES:
                f = f + self.LETTER_FORCES[ch]
        return f

    # --------------------------------------------------------
    # FORCE-WEIGHTED GLYPH SAMPLING (OPTION C)
    # --------------------------------------------------------
    def _glyph_sampling_weights(self, raw_force: ForceVector) -> List[float]:
        """
        Build a weight per glyph based on alignment with the raw word force.
        """
        raw = raw_force.as_dict()
        raw_mag = raw_force.magnitude()
        if raw_mag == 0.0:
            # If the word has no recognizable letters, use uniform weights.
            return [1.0 for _ in self.ALPHABET]

        weights: List[float] = []
        for ch in self.ALPHABET:
            lf = self.LETTER_FORCES[ch].as_dict()
            # Cosine-like alignment: dot / (|raw| * |lf|)
            dot = sum(raw[name] * lf[name] for name in FORCE_NAMES)
            lf_mag = self.LETTER_FORCES[ch].magnitude()
            if lf_mag == 0.0:
                w = 0.0
            else:
                w = max(0.0, dot / (raw_mag * lf_mag))
            # Add a small floor so nothing is completely impossible
            weights.append(w + 0.01)
        return weights

    def _sample_glyphs_for_word(self, word: str) -> str:
        """
        Sample 1–12 glyphs from the alphabet, weighted by the word's raw force.
        """
        clean = self._sanitize_word(word)
        if not clean:
            clean = "X"

        # Decide length: 1–12, biased by word length but capped
        length = max(1, min(12, len(clean)))

        raw_force = self._compute_raw_word_force(clean)
        weights = self._glyph_sampling_weights(raw_force)
        total_w = sum(weights)
        if total_w == 0.0:
            # Fallback to uniform
            weights = [1.0 for _ in self.ALPHABET]
            total_w = float(len(weights))

        # Normalize
        probs = [w / total_w for w in weights]

        glyphs = []
        for _ in range(length):
            r = random.random()
            acc = 0.0
            for ch, p in zip(self.ALPHABET, probs):
                acc += p
                if r <= acc:
                    glyphs.append(ch)
                    break
        return ''.join(glyphs)

    # --------------------------------------------------------
    # GLYPHS → FORCES / STRUCTURE
    # --------------------------------------------------------
    def _compute_glyph_force(self, glyphs: str) -> ForceVector:
        f = ForceVector()
        for ch in glyphs:
            if ch in self.LETTER_FORCES:
                f = f + self.LETTER_FORCES[ch]
        return f

    def _build_shell_from_glyphs(self, glyphs: str) -> Dict[str, List[int]]:
        shell: Dict[str, List[int]] = {}
        for i, ch in enumerate(glyphs):
            shell.setdefault(ch, []).append(i)
        return shell

    def _build_semantic_vector_from_glyphs(self, glyphs: str) -> List[float]:
        vec = [0.0] * len(self.ALPHABET)
        for ch in glyphs:
            if ch in self.ALPHABET:
                idx = self.ALPHABET.index(ch)
                vec[idx] += 1.0
        return vec

    # --------------------------------------------------------
    # BUILD BLOCK FROM WORD (TWO-LANGUAGE MODEL)
    # --------------------------------------------------------
    def _build_block_from_word(self, word: str) -> MathBlock:
        # Surface word (meaning layer)
        surface = word

        # Internal glyph identity (force layer)
        glyphs = self._sample_glyphs_for_word(surface)

        # Forces and structure from glyphs
        forces = self._compute_glyph_force(glyphs)
        core = forces.magnitude()
        shell = self._build_shell_from_glyphs(glyphs)
        semantic_vector = self._build_semantic_vector_from_glyphs(glyphs)

        block = MathBlock(
            word=surface,
            id=self.next_id,
            glyphs=glyphs,
            core=core,
            shell=shell,
            semantic_vector=semantic_vector,
            forces=forces,
        )
        self.next_id += 1
        return block

    # --------------------------------------------------------
    # GLYPH FIRMING / MUTATION
    # --------------------------------------------------------
    def _firm_glyphs(self, block: MathBlock, identity: Any, memory: Any, world: Any) -> str:
        """
        Simple glyph firming:
          - drift: occasional swap
          - chaos: occasional random mutation
          - echo: reinforce repeats
          - clarity: reduce noise (favor more common glyphs in the block)
        This is intentionally light; you can deepen it later.
        """
        glyphs = list(block.glyphs)
        if not glyphs:
            return block.glyphs

        f = block.forces.as_dict()
        drift = f["drift"]
        chaos = f["chaos"]
        echo = f["echo"]
        clarity = f["clarity"]

        # Drift: swap adjacent glyphs with small probability
        if random.random() < min(0.3, drift):
            i = random.randrange(0, len(glyphs) - 1) if len(glyphs) > 1 else 0
            j = min(len(glyphs) - 1, i + 1)
            glyphs[i], glyphs[j] = glyphs[j], glyphs[i]

        # Chaos: random mutation of one glyph
        if random.random() < min(0.3, chaos):
            idx = random.randrange(0, len(glyphs))
            glyphs[idx] = random.choice(self.ALPHABET)

        # Echo: duplicate a glyph if echo is high and length < 12
        if random.random() < min(0.3, echo) and len(glyphs) < 12:
            idx = random.randrange(0, len(glyphs))
            glyphs.insert(idx, glyphs[idx])

        # Clarity: bias toward the most frequent glyph in the block
        if random.random() < min(0.3, clarity):
            freq: Dict[str, int] = {}
            for g in glyphs:
                freq[g] = freq.get(g, 0) + 1
            if freq:
                dominant = max(freq.items(), key=lambda kv: kv[1])[0]
                # Nudge one random glyph toward the dominant
                idx = random.randrange(0, len(glyphs))
                glyphs[idx] = dominant

        # Enforce 1–12 glyphs
        if len(glyphs) > 12:
            glyphs = glyphs[:12]
        if len(glyphs) == 0:
            glyphs = ["X"]

        return ''.join(glyphs)

    # --------------------------------------------------------
    # MAIN UPDATE ENTRY
    # --------------------------------------------------------
    def update_block(self, block: MathBlock, identity: Any, memory: Any, world: Any) -> None:
        """
        Update a single block:
          - recompute forces from current glyphs
          - firm glyphs based on forces/world/memory/identity
          - recompute forces after firming
          - advance developmental ladder
        """
        # Recompute forces from current glyphs
        block.forces = self._compute_glyph_force(block.glyphs)
        block.core = block.forces.magnitude()
        block.shell = self._build_shell_from_glyphs(block.glyphs)
        block.semantic_vector = self._build_semantic_vector_from_glyphs(block.glyphs)

        # Firm glyphs
        new_glyphs = self._firm_glyphs(block, identity, memory, world)
        if new_glyphs != block.glyphs:
            block.glyphs = new_glyphs
            block.flow_flag = True

        # Recompute forces after firming
        block.forces = self._compute_glyph_force(block.glyphs)
        block.core = block.forces.magnitude()
        block.shell = self._build_shell_from_glyphs(block.glyphs)
        block.semantic_vector = self._build_semantic_vector_from_glyphs(block.glyphs)

        # Developmental ladder
        self._advance(block, identity, memory, world)

    def step(self, identity: Any = None, memory: Any = None, world: Any = None) -> Dict[str, Any]:
        """
        Optional heartbeat:
          - updates all blocks
          - returns a viewer-friendly snapshot
        """
        identity = identity or {}
        memory = memory or {}
        world = world or {}

        for block in self.blocks_by_word.values():
            self.update_block(block, identity, memory, world)

        out_blocks = []
        for block in self.blocks_by_word.values():
            out_blocks.append({
                "word": block.word,
                "id": block.id,
                "glyphs": block.glyphs,
                "forces": block.forces.as_dict(),
                "level": block.level,
                "micro_gate": block.micro_gate,
                "ascended": block.ascended,
                "canon": block.canon,
                "flow": block.flow_flag,
            })

        return {
            "count": len(out_blocks),
            "blocks": out_blocks,
        }

    # --------------------------------------------------------
    # DEVELOPMENTAL LADDER
    # --------------------------------------------------------
    def _advance(self, block: MathBlock, identity: Any, memory: Any, world: Any) -> None:
        if block.ascended:
            return

        if self._gate_pass(block):
            block.micro_gate += 1
            block.flow_flag = True

            if block.micro_gate >= self.GATES:
                block.level += 1
                block.micro_gate = 0
                block.flow_flag = True

        if block.level >= self.LEVELS:
            self._try_ascend(block)

    def _gate_pass(self, block: MathBlock) -> bool:
        """
        Simple micro-gate check:
          - cycles through force names
          - compares current force value to level threshold
        """
        f = block.forces.as_dict()
        lvl = block.level
        idx = block.micro_gate
        name = FORCE_NAMES[idx % len(FORCE_NAMES)]
        val = f[name]
        req = self.thresholds[lvl][name]
        return val >= req

    def _try_ascend(self, block: MathBlock) -> None:
        """
        Ascend when level is max and average force is high enough.
        Locks glyphs as canon.
        """
        avg_force = sum(block.forces.as_dict().values()) / len(FORCE_NAMES)
        if avg_force >= 1.5:  # tunable
            block.ascended = True
            block.canon = True
            block.flow_flag = True
