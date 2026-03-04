# organs/mathblock_source.py
# SAFE, INERT mathblock reservoir + example generator

class MathBlockSource:
    """
    Provides large sets of mathblocks for:
      - reservoir (stable)
      - example sets (dynamic)
    This organ is SAFE and INERT until explicitly called.
    """

    def __init__(self, creature, reservoir_size=40, blocks_per_word=3):
        self.creature = creature
        self.reservoir_size = reservoir_size
        self.blocks_per_word = blocks_per_word

        # Pre-generate reservoir mathblocks
        self.reservoir = self._generate_reservoir()

    # ----------------------------------------------------
    # INTERNAL GENERATION
    # ----------------------------------------------------
    def _generate_reservoir(self):
        """
        Creates a stable reservoir of mathblocks.
        SAFE: does not affect any other organ.
        """
        reservoir = []
        for i in range(self.reservoir_size):
            block = {
                "id": f"MB{i}",
                "spark": 0.0,
                "drift": 0.0,
                "echo": 0.0,
                "pressure": 0.0,
                "symbol": f"σ{i}",
                "category": "neutral",
                "surface": "smooth",
            }
            reservoir.append(block)
        return reservoir

    # ----------------------------------------------------
    # PUBLIC API (SAFE)
    # ----------------------------------------------------
    def get_reservoir(self):
        """Returns the stable reservoir. SAFE."""
        return self.reservoir

    def generate_example_blocks(self, words):
        """
        Generates mathblocks for example words.
        SAFE: not used unless explicitly called.
        """
        example_sets = {}
        for w in words:
            blocks = []
            for i in range(self.blocks_per_word):
                blocks.append({
                    "word": w,
                    "spark": 0.0,
                    "drift": 0.0,
                    "echo": 0.0,
                    "pressure": 0.0,
                    "symbol": f"{w[:2]}_{i}",
                    "category": "example",
                    "surface": "bouncy",
                })
            example_sets[w] = blocks
        return example_sets
