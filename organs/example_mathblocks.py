# organs/example_mathblocks.py
# Assigns math blocks to example-pool words.
# SAFE: does nothing unless explicitly called.

class ExampleMathBlocks:
    """
    Assigns math blocks to words from the ExamplePool.
    This organ is SAFE and INERT until another organ requests mappings.
    """

    def __init__(self, creature, blocks_per_word=3):
        self.creature = creature
        self.blocks_per_word = blocks_per_word
        self.pool = creature.example_pool  # must be installed later
        self.assignments = {}  # { story_type: { word: [mathblocks...] } }

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def get_story_type_blocks(self, story_type):
        """Return mathblock assignments for all words in a story type."""
        if story_type not in self.assignments:
            self.assignments[story_type] = self._assign_for_story_type(story_type)
        return self.assignments[story_type]

    def get_word_blocks(self, story_type, word):
        """Return mathblocks for a single word."""
        story_map = self.get_story_type_blocks(story_type)
        return story_map.get(word.lower(), [])

    # ------------------------------------------------------------
    # INTERNAL: Assign blocks for a whole story type
    # ------------------------------------------------------------
    def _assign_for_story_type(self, story_type):
        sentences = self.pool.get_sentences(story_type)
        words = self._extract_words(sentences)
        return { w: self._generate_blocks(w) for w in words }

    # ------------------------------------------------------------
    # INTERNAL: Extract normalized words
    # ------------------------------------------------------------
    def _extract_words(self, sentences):
        import re
        words = set()
        for s in sentences:
            tokens = re.findall(r"[a-zA-Z']+", s.lower())
            words.update(tokens)
        return sorted(words)

    # ------------------------------------------------------------
    # INTERNAL: Generate mathblocks for a word
    # ------------------------------------------------------------
    def _generate_blocks(self, word):
        blocks = []
        for i in range(self.blocks_per_word):
            blocks.append({
                "word": word,
                "symbol": f"{word[:2]}_{i}",
                "spark": 0.0,
                "drift": 0.0,
                "echo": 0.0,
                "pressure": 0.0,
                "category": "example",
                "surface": "bouncy"
            })
        return blocks
