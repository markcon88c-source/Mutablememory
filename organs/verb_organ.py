import random

class VerbOrgan:
    def __init__(self):
        self.verbs = [
            "moves through",
            "rests in",
            "leans toward",
            "circles",
            "touches",
            "drifts across",
            "waits beside",
            "breathes within",
            "settles near"
        ]

    def generate(self, state):
        return random.choice(self.verbs)
