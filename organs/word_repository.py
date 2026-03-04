class WordRepository:
    """
    A large reservoir of possible words, including character names.
    Names are stored separately and imported more rarely.
    """

    def __init__(self):
        self.words = set()
        self.names = set()
        self.generated_names = set()

    def load_default_words(self):
        base_words = [
            "river", "stone", "memory", "shadow", "light", "path", "gate",
            "dream", "story", "mark", "spirit", "root", "branch", "echo",
            "pattern", "drift", "spark", "focus", "pause", "seed", "myth",
            "symbol", "intent", "meaning", "canon", "archive", "world",
            "place", "time", "truth", "value", "purpose", "legend",
            "wind", "fire", "water", "earth", "sky", "night", "day",
        ]

        for w in base_words:
            self.words.add(w)

        # Canonical character names
        canonical_names = [
            "Dawn", "Cash", "Gozer", "Janort", "Thembloom"
        ]

        for n in canonical_names:
            self.names.add(n)

    def add_user_names(self, names):
        for n in names:
            self.names.add(n)

    def add_generated_name(self, name):
        self.generated_names.add(name)

    def get_random_word(self):
        import random
        if not self.words:
            return None
        return random.choice(list(self.words))

    def get_random_name(self):
        import random
        all_names = list(self.names | self.generated_names)
        if not all_names:
            return None
        return random.choice(all_names)
