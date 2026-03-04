import random

class PersonalityOrgan:
    """
    A simple personality organ with:
      - core traits
      - driftable modifiers
      - personality vector
      - voice summary
    """

    def __init__(self):
        self.traits = {
            "curiosity": 0.5,
            "steadiness": 0.5,
            "warmth": 0.5,
            "intensity": 0.5,
            "playfulness": 0.5
        }

        self.last_voice = "neutral"

    def apply_drift(self, drift_intensity):
        """
        Drift modifies traits slightly.
        """
        for k in self.traits:
            delta = random.uniform(-0.1, 0.1) * drift_intensity
            self.traits[k] += delta

            if self.traits[k] < 0.0:
                self.traits[k] = 0.0
            if self.traits[k] > 1.0:
                self.traits[k] = 1.0

    def personality_vector(self):
        """
        Return a simple vector representation.
        """
        return [
            self.traits["curiosity"],
            self.traits["steadiness"],
            self.traits["warmth"],
            self.traits["intensity"],
            self.traits["playfulness"]
        ]

    def compute_voice(self, mood, emphasis):
        """
        Determine a personality 'voice' for this cycle.
        """
        c = self.traits["curiosity"]
        s = self.traits["steadiness"]
        w = self.traits["warmth"]
        i = self.traits["intensity"]
        p = self.traits["playfulness"]

        if emphasis and i > 0.6:
            voice = "bright-intense"
        elif mood == "calm" and s > 0.6:
            voice = "steady-calm"
        elif mood == "curious" and c > 0.6:
            voice = "curious-open"
        elif p > 0.6:
            voice = "playful-light"
        elif w > 0.6:
            voice = "warm-gentle"
        else:
            voice = "neutral"

        self.last_voice = voice
        return voice

    def packet(self):
        """
        Return a summary packet for the viewer or English organ.
        """
        return {
            "traits": dict(self.traits),
            "voice": self.last_voice
        }
