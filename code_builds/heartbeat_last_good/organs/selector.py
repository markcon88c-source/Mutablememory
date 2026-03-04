import random

class SelectorOrgan:
    """
    Chooses which internal signal should dominate the cycle:
      - mood
      - drift
      - memory
      - personality
      - worldbuilding
      - emphasis
    Produces a selector packet for the English organ.
    """

    def __init__(self):
        self.last_choice = "mood"

    def choose(self, mood, drift_shifted, memory_score,
               personality_voice, emphasis):
        """
        Decide which signal dominates.
        Returns:
          - choice (string)
          - reason (string)
        """

        weights = {}

        # Mood dominates when calm or curious
        if mood in ("calm", "curious"):
            weights["mood"] = 0.3
        else:
            weights["mood"] = 0.15

        # Drift dominates when patterns shift
        if drift_shifted:
            weights["drift"] = 0.35
        else:
            weights["drift"] = 0.1

        # Memory dominates when score is high
        if memory_score > 0.7:
            weights["memory"] = 0.3
        else:
            weights["memory"] = 0.1

        # Personality dominates when voice is strong
        if personality_voice in (
            "bright-intense",
            "curious-open",
            "playful-light",
            "warm-gentle"
        ):
            weights["personality"] = 0.25
        else:
            weights["personality"] = 0.1

        # Emphasis overrides everything lightly
        if emphasis:
            weights["emphasis"] = 0.4
        else:
            weights["emphasis"] = 0.05

        # Normalize weights
        total = sum(weights.values())
        norm = {}
        for k in weights:
            norm[k] = weights[k] / total

        # Weighted random choice
        r = random.random()
        acc = 0.0
        choice = "mood"

        for k in norm:
            acc += norm[k]
            if r <= acc:
                choice = k
                break

        self.last_choice = choice

        reason = "Chosen because {} signal was strongest".format(choice)

        return choice, reason

    def packet(self, choice, reason):
        """
        Return a selector packet for the English organ.
        """
        return {
            "selector_choice": choice,
            "selector_reason": reason
        }
