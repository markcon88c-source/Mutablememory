from decimal import Decimal, getcontext
from typing import List, Dict, Any, Optional
from .math_block import MathBlock

getcontext().prec = 24


class STMOrgan:
    """
    Short-term memory spine with:
    - 11 levels (L1–L11)
    - nonlinear, math-block-assigned gate targets
    - micro-precision windows
    - cooldown per item
    - 1 promotion per tick
    - 1 story seed per 50 ticks (L11 entries)
    """

    def __init__(self, math_block: Optional[MathBlock] = None):
        self.math_block = math_block or MathBlock()

        # Levels: 0..10 represent L1..L11
        self.levels: List[List[Dict[str, Any]]] = [[] for _ in range(11)]

        # Promotion control
        self.max_promotions_per_tick = 1
        self.story_seed_interval = 50
        self._ticks = 0
        self._story_seed_counter = 0

        # Gate tolerance: how close meaning must be to target
        self.gate_tolerance = Decimal("0.000000000000500")

        # Cooldown in ticks before an item can move again
        self.cooldown_ticks = 12

    def _to_decimal(self, value: float) -> Decimal:
        return Decimal(str(value))

    def _can_promote(self, item: Dict[str, Any], level_index: int) -> bool:
        """
        Decide if an item at level_index can move to the next level.
        Uses:
        - exact target from math block
        - micro-precision window
        - cooldown
        """
        if level_index >= 10:
            # Already at top (L11)
            return False

        if item.get("cooldown", 0) > 0:
            return False

        meaning = self._to_decimal(item.get("meaning", 0.0))
        resonance = self._to_decimal(item.get("resonance", 0.0))
        polarity = self._to_decimal(item.get("polarity", 0.0))

        # Nonlinear exact target from math block
        target = self.math_block.target_for_level(level_index + 1)

        # Must be within a tiny window of the target
        if abs(meaning - target) > self.gate_tolerance:
            return False

        # Resonance and polarity stability
        if resonance < Decimal("0.400000000000000"):
            return False

        if abs(polarity) < Decimal("0.250000000000000"):
            return False

        return True

    def _tick_cooldowns(self):
        for level in self.levels:
            for item in level:
                if item.get("cooldown", 0) > 0:
                    item["cooldown"] -= 1

    def step(self, word_snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Called once per critter tick.

        word_snapshots: list of dicts like:
        {
            "word": str,
            "meaning": float,
            "resonance": float,
            "polarity": float,
        }
        """
        self._ticks += 1
        self._tick_cooldowns()

        # Ingest new words into L1
        for w in word_snapshots:
            item = {
                "word": w.get("word"),
                "meaning": self._to_decimal(w.get("meaning", 0.0)),
                "resonance": self._to_decimal(w.get("resonance", 0.0)),
                "polarity": self._to_decimal(w.get("polarity", 0.0)),
                "cooldown": self.cooldown_ticks,
                "born_tick": self._ticks,
            }
            self.levels[0].append(item)

        promotions_this_tick = 0
        story_seeds_this_tick: List[Dict[str, Any]] = []

        # Try to promote from top down (so higher levels resolve first)
        for level_index in reversed(range(10)):  # 0..9 (L1..L10)
            if promotions_this_tick >= self.max_promotions_per_tick:
                break

            level = self.levels[level_index]
            next_level = self.levels[level_index + 1]

            for item in level:
                if promotions_this_tick >= self.max_promotions_per_tick:
                    break

                if self._can_promote(item, level_index):
                    # Remove from current level
                    level.remove(item)

                    # Move to next level
                    item["cooldown"] = self.cooldown_ticks
                    next_level.append(item)
                    promotions_this_tick += 1

                    # If we just entered L11, maybe emit a story seed
                    if level_index + 1 == 10:  # moved into index 10 (L11)
                        self._story_seed_counter += 1
                        if self._story_seed_counter >= self.story_seed_interval:
                            self._story_seed_counter = 0
                            story_seeds_this_tick.append(item)

        return {
            "tick": self._ticks,
            "levels": self.levels,
            "story_seeds": story_seeds_this_tick,
        }
