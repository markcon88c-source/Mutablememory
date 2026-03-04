import random

class Avoidance:
    """
    Simple avoidance organ.
    Produces an avoidance level each cycle.
    """

    def __init__(self):
        self.rng = random.Random()
        self.level = 0.0
        self.inertia = 0.75

    def update(self):
        """
        Returns a dict with avoidance level.
        """
        if self.rng.random() > self.inertia:
            self.level = random.uniform(0.0, 1.0)

        return {"level": self.level}
