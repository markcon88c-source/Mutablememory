import random
from decimal import Decimal, getcontext

getcontext().prec = 24

class WorldOrgan:
    def __init__(self):
        self.rng = random.Random()
        self.places = [
            "hollow gate",
            "quiet stair",
            "wind corridor",
            "soft field",
            "old stone",
            "narrow path",
            "dusk chamber",
            "low archway",
            "still water",
            "warm dust"
        ]

    def _tone(self):
        v = Decimal(str(self.rng.random()))
        return v

    def _weather(self):
        v = Decimal(str(self.rng.random()))
        return v

    def step(self, thought):
        place = self.rng.choice(self.places)
        tone = self._tone()
        weather = self._weather()
        return {
            "place": place,
            "tone": tone,
            "weather": weather
        }
