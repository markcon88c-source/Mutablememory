# organs/s_levels_organ.py
# S-Levels: Story Levels (11 major x 17 micro)
# With story-type pushback/acceptance integrated

from typing import Dict, Any


class SLevelsOrgan:
    """
    Standalone Story Levels system.
    - Tracks S-level (1–11) and micro-level (0–16) per token/word
    - Story types influence ascension (boost or pushback)
    - Fully separate from the main story engine
    """

    def __init__(self):
        # word -> {"level": int, "micro": int, "score": float, "story_type": str}
        self.levels: Dict[str, Dict[str, Any]] = {}
        self.cycle = 0

        self.MAX_LEVEL = 11
        self.MAX_MICRO = 16

        # Preferred story type per S-level
        self.preferred = {
            1: "dream",
            2: "mystery",
            3: "drama",
            4: "action",
            5: "action",
            6: "drama",
            7: "mythic",
            8: "mythic",
            9: "epic",
            10: "epic",
            11: "mythic",
        }

        # Adjacent types (soft acceptance)
        self.adjacent = {
            "dream": ["mystery", "drama"],
            "mystery": ["dream", "drama"],
            "drama": ["mystery", "action"],
            "action": ["drama", "mythic"],
            "mythic": ["action", "epic"],
            "epic": ["mythic"],
        }

    # ------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------

    def _ensure_entry(self, word: str, story_type: str = None):
        """Ensure the word exists in the table and store story type."""
        if word not in self.levels:
            self.levels[word] = {
                "level": 1,
                "micro": 0,
                "score": 0.0,
                "story_type": story_type or "unknown",
            }
        else:
            if story_type:
                self.levels[word]["story_type"] = story_type

    def _story_type_modifier(self, story_type: str, level: int) -> float:
        """Return boost or pushback based on story-type alignment."""
        preferred = self.preferred.get(level)

        if story_type == preferred:
            return +0.20

        if story_type in self.adjacent.get(preferred, []):
            return +0.05

        return -0.10

    def _apply_delta(self, word: str, delta: float):
        """Apply score delta and translate into micro/major level changes."""
        entry = self.levels[word]
        entry["score"] += delta

        # Ascend
        while entry["score"] >= 1.0:
            entry["score"] -= 1.0
            entry["micro"] += 1

            if entry["micro"] > self.MAX_MICRO:
                entry["micro"] = 0
                entry["level"] = min(self.MAX_LEVEL, entry["level"] + 1)

        # Descend
        while entry["score"] <= -1.0:
            entry["score"] += 1.0
            entry["micro"] -= 1

            if entry["micro"] < 0:
                entry["micro"] = self.MAX_MICRO
                entry["level"] = max(1, entry["level"] - 1)

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------

    def step_from_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Update S-levels from a story event."""
        self.cycle += 1

        word = event.get("word")
        story_type = event.get("story_type")

        if not word:
            return {"cycle": self.cycle, "levels": self.levels}

        self._ensure_entry(word, story_type)
        entry = self.levels[word]

        base = 0.30
        modifier = self._story_type_modifier(story_type, entry["level"])

        self._apply_delta(word, base + modifier)

        return {
            "cycle": self.cycle,
            "levels": dict(self.levels),
        }

    def get_state(self) -> Dict[str, Any]:
        return {
            "cycle": self.cycle,
            "levels": dict(self.levels),
        }
