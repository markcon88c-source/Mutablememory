# organs/l_levels.py

from typing import Dict, Optional

class LLevelsOrgan:
    """
    L-Levels Organ.
    Stores a simple integer level per word.
    Loader expects it to accept the creature reference.
    """

    def __init__(self, creature=None):
        """
        Accept the creature reference because the loader passes it.
        """
        self.creature = creature
        self.levels: Dict[str, int] = {}

    def set_level(self, word: str, level: int):
        """
        Set the L-level for a word.
        """
        self.levels[word] = level

    def get_level(self, word: str) -> Optional[int]:
        """
        Get the L-level for a word, or None if missing.
        """
        return self.levels.get(word)

    def has_word(self, word: str) -> bool:
        """
        Check if a word has an L-level entry.
        """
        return word in self.levels

    def all_levels(self) -> Dict[str, int]:
        """
        Return the entire L-level mapping.
        """
        return dict(self.levels)
