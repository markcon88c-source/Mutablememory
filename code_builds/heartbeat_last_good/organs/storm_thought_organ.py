import random

class StormThoughtOrgan:
    def __init__(self):
        self.pool_a = ["crackling", "charged", "rising", "shattered", "fierce", "spiraling"]
        self.pool_b = ["current", "pulse", "stormline", "arc", "surge", "flare"]

    def generate(self, state):
        intensity = state["pressures"].get("storm", 0.0)
        if intensity < 0.25:
            return ""
        a = random.choice(self.pool_a)
        b = random.choice(self.pool_b)
        return f"{a} {b}"
