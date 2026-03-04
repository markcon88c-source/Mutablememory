# organs/mathblocks.py

from dataclasses import dataclass
from typing import Dict, Optional, Any
import random


@dataclass
class MathBlock:
    """
    A single math block representing a word's symbolic/force identity.
    """
    word: str
    symbol: str
    force: float
    category: str


class MathBlocks:
    """
    Global MathBlocks Organ
    - Stores MathBlock packets
    - Auto-generates blocks for new thoughts
    - Provides a stable .step() interface for story organs
    - Now includes get_block(word) for universal access
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.blocks: Dict[str, MathBlock] = {}
        self.rng = random.Random()
        self._load_default_blocks()

    def _load_default_blocks(self):
        starter = {
            "the": MathBlock("the", "Θ", 0.1, "function"),
            "and": MathBlock("and", "∧", 0.2, "function"),
            "I":   MathBlock("I",   "ι", 0.5, "identity"),
            "you": MathBlock("you", "γ", 0.5, "identity"),
        }
        self.blocks.update(starter)

    def _auto_generate(self, word: str):
        symbol = random.choice(["Θ", "∧", "ι", "γ", "Σ", "Φ", "🔥", "🌀", "🌫"])
        force = float(self.rng.random())
        category = "unknown"
        return MathBlock(word, symbol, force, category)

    # ---------------------------------------------------------
    # UNIVERSAL ACCESSOR (required by ExamplePackOrgan)
    # ---------------------------------------------------------
    def get_block(self, word: str):
        """
        Return the MathBlock for a word.
        Auto-generates it if it does not exist.
        """
        if word not in self.blocks:
            self.blocks[word] = self._auto_generate(word)
        return self.blocks[word]

    # ---------------------------------------------------------
    # HEARTBEAT VIEWER INTERFACE
    # ---------------------------------------------------------
    def step(self, thought: str, world: Optional[Dict[str, Any]] = None, heart: Optional[Dict[str, Any]] = None):
        """
        Heartbeat:
        - Ensure the current thought has a MathBlock
        - Return a viewer-friendly LIST of blocks
        """

        if thought and thought not in self.blocks:
            self.blocks[thought] = self._auto_generate(thought)

        # convert internal dict → list of viewer-ready dicts
        block_list = []
        for word, block in self.blocks.items():
            block_list.append({
                "word": word,
                "forces": {
                    "spark": block.force,
                    "drift": block.force * 0.8,
                    "echo": block.force * 0.6,
                    "chaos": block.force * 0.4,
                    "clarity": block.force * 0.5,
                    "memory": block.force * 0.7,
                    "pressure": block.force * 0.9,
                },
                "glyph": block.symbol,
            })

        return {
            "blocks": block_list,
            "count": len(block_list)
        }
