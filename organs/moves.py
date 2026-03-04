import random

class Moves:
    """
    Movement organ that returns both an action and an intensity.
    """

    def __init__(self):
        self.rng = random.Random()

        self.actions = [
            "still",
            "shift",
            "step",
            "turn",
            "reach",
            "wander"
        ]

        self.last = "still"
        self.inertia = 0.7

    def update(self):
        """
        Returns:
            {
                "action": <str>,
                "intensity": <float>
            }
        """
        # Choose action with inertia
        if self.rng.random() > self.inertia:
            self.last = self.rng.choice(self.actions)

        # Convert action into intensity
        if self.last == "still":
            intensity = 0.0
        elif self.last == "shift":
            intensity = 0.2
        elif self.last == "step":
            intensity = 0.4
        elif self.last == "turn":
            intensity = 0.5
        elif self.last == "reach":
            intensity = 0.7
        else:  # wander
            intensity = 0.9

        return {
            "action": self.last,
            "intensity": intensity
        }
