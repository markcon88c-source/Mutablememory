import random

class ReactionOrgan:
    def __init__(self):
        self.reactions = [
            "The air shifts.",
            "A quiet echo answers.",
            "The field remembers.",
            "Something stirs beneath.",
            "The horizon softens.",
            "A faint warmth rises.",
            "Stillness deepens.",
            "The valley listens."
        ]

    def generate(self, state):
        return random.choice(self.reactions)
