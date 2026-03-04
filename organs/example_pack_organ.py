from organs.mathblocks import MathBlocks

class ExamplePackOrgan:
    """
    Stores genre-specific example sets and converts them into
    MathBlock sequences so the creature can brush up against
    structural, force-aware patterns.
    """

    def __init__(self):
        self.packs = {}
        self.mathblocks = MathBlocks()

        # load built-in packs
        self._load_builtin_comedy_pack()

        # convert all packs into MathBlock sequences
        self._assign_mathblocks_to_all_packs()

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def get_pack(self, name):
        """Return a list of examples (each example is a list of MathBlocks)."""
        return self.packs.get(name, [])

    def list_packs(self):
        return list(self.packs.keys())

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _assign_mathblocks_to_all_packs(self):
        """Convert every example sentence into a list of MathBlocks."""
        for pack_name, examples in self.packs.items():
            converted = []
            for sentence in examples:
                words = sentence.split()
                blocks = [self.mathblocks.get_block(word) for word in words]
                converted.append(blocks)
            self.packs[pack_name] = converted

    # ---------------------------------------------------------
    # BUILT-IN PACKS
    # ---------------------------------------------------------

    def _load_builtin_comedy_pack(self):
        comedy_examples = [
            "The stone tried to look serious but kept giggling.",
            "Memory forgot what it was explaining halfway through.",
            "The spark tripped over its own metaphor.",
            "Pressure knocked politely before panicking.",
            "The river apologized for being too dramatic.",
            "Dreams attempted a speech but fell asleep mid-sentence.",
            "The shadow insisted it wasn’t following anyone just coincidentally nearby.",
            "A thought sprinted ahead realized it was wrong and jogged back awkwardly.",
            "The gremlin raised its hand to ask a question it immediately forgot.",
            "The wind tried to whisper a secret but shouted it by accident.",
            "The idea strutted in confidently then realized it had the wrong meeting.",
            "The sentence cleared its throat three times before giving up.",
            "The metaphor tried to be deep but slipped on its own symbolism.",
            "The emotion arrived early panicked and hid behind a chair.",
            "The concept waved enthusiastically at someone who wasn’t waving at it.",
            "The memory claimed it was totally reliable while sweating nervously.",
            "The spark attempted a dramatic entrance but tripped over the punctuation.",
            "The gremlin tried to help but only made things funnier.",
            "The story beat missed its cue and improvised something chaotic.",
            "The idea knocked entered apologized left and knocked again."
        ]

        self.packs["comedy"] = comedy_examples
