import random

class ConsequenceOrgan:
    """
    Computes narrative consequences based on:
      - mood
      - drift
      - memory score
      - selector choice
      - worldbuilding alignment
      - emphasis
    Produces:
      - consequence_score
      - consequence_reason
      - packet
    """

    def __init__(self):
        self.last_score = 0.0
        self.last_reason = "none"

    def compute_base(self, mood, drift_shifted, emphasis):
        """
        Base consequence from mood, drift, and emphasis.
        """
        score = 0.0

        if mood in ("chaotic", "bright"):
            score += 0.3
        elif mood in ("curious", "focused"):
            score += 0.2
        else:
            score += 0.1

        if drift_shifted:
            score += 0.3
        else:
            score += 0.1

        if emphasis:
            score += 0.2

        return score

    def memory_influence(self, memory_score):
        """
        Memory score influences consequences.
        """
        if memory_score > 0.8:
            return 0.3
        if memory_score > 0.5:
            return 0.2
        if memory_score > 0.2:
            return 0.1
        return 0.05

    def selector_influence(self, selector_choice):
        """
        Selector choice affects consequence weight.
        """
        if selector_choice == "emphasis":
            return 0.3
        if selector_choice == "drift":
            return 0.25
        if selector_choice == "memory":
            return 0.2
        if selector_choice == "personality":
            return 0.15
        return 0.1

    def worldbuilding_influence(self, alignment):
        """
        World alignment affects consequence tone.
        """
        if alignment == "volatile":
            return 0.3
        if alignment == "shadowed":
            return 0.25
        if alignment == "ancient":
            return 0.2
        if alignment == "bright":
            return 0.15
        return 0.1

    def compute(self, mood, drift_shifted, memory_score,
                selector_choice, alignment, emphasis):
        """
        Main consequence computation.
        Returns:
          - score
          - reason
        """

        base = self.compute_base(mood, drift_shifted, emphasis)
        mem = self.memory_influence(memory_score)
        sel = self.selector_influence(selector_choice)
        wld = self.worldbuilding_influence(alignment)

        score = base + mem + sel + wld

        noise = random.uniform(0.0, 0.1)
        score += noise

        if score > 1.2:
            reason = "STRONG CONSEQUENCE"
        elif score > 0.8:
            reason = "MODERATE CONSEQUENCE"
        elif score > 0.5:
            reason = "LIGHT CONSEQUENCE"
        else:
            reason = "MINIMAL CONSEQUENCE"

        self.last_score = score
        self.last_reason = reason

        return score, reason

    def packet(self):
        """
        Return a consequence packet for the viewer or state.
        """
        return {
            "consequence_score": self.last_score,
            "consequence_reason": self.last_reason
        }
