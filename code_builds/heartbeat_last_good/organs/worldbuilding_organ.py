import random

class WorldbuildingOrgan:
    def __init__(self):
        self.seed_s = ["ashen ridge", "quiet vale", "low lantern", "hollow path"]
        self.seed_l = ["the old horizon", "the first lantern", "the deep field"]

    def generate_s(self, state):
        return random.choice(self.seed_s)

    def generate_l(self, state):
        return random.choice(self.seed_l)
