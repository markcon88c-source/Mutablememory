import random
from decimal import Decimal, getcontext

getcontext().prec = 24

class ThoughtOrgan:
    def __init__(self):
        self.rng = random.Random()
        self.word_pool = [
            "soft", "gate", "hollow", "dust",
            "warm", "stone", "still", "field",
            "low", "arch", "dusk", "path",
            "quiet", "wind", "echo", "root"
        ]

    def _pulse(self):
        v = Decimal(str(self.rng.random()))
        return v

    def _tone(self):
        v = Decimal(str(self.rng.random()))
        return v

    def _words(self):
        count = self.rng.randint(1, 4)
        out = []
        for _ in range(count):
            out.append(self.rng.choice(self.word_pool))
        return out

    def step(self):
        return {
            "words": self._words(),
            "pulse": self._pulse(),
            "tone": self._tone()
        }
