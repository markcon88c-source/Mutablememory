import random

class WorldbuildingOrgan:
    """
    Generates small worldbuilding fragments.
    """

    def __init__(self):
        self.fragments = [
            "a quiet valley",
            "a shifting corridor",
            "a forgotten shrine",
            "a bright field",
            "a chaotic market"
        ]

    def generate(self):
        return random.choice(self.fragments)

    def generate_many(self, n):
        out = []
        for _ in range(n):
            out.append({
                "fragment": self.generate(),
                "alignment": random.random()
            })
        return out

    def sample_for_viewer(self, packets):
        if not packets:
            return "empty world"
        return packets[0]["fragment"]
