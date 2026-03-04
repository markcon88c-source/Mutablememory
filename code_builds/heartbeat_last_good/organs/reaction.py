import random

class Reaction:
    """
    Simple reaction organ.
    Produces a reaction spike each cycle.
    """

    def __init__(self):
        self.rng = random.Random()
        self.spike = 0.0
        self.inertia = 0.65

    def update(self):
        """
        Returns a dict with reaction spike.
        """
        if self.rng.random() > self.inertia:
            self.spike = random.uniform(0.0, 1.0)

        return {"spike": self.spike}
