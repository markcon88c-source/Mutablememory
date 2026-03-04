class ForceStabilityGate:
    """
    Evaluates whether the six forces produce a stable enough pattern
    for the creature to form a sentence safely.
    """

    def __init__(self):
        # Thresholds can be tuned later
        self.accept_threshold = 0.65
        self.not_yet_threshold = 0.35

    def compute_stability(self, forces):
        """
        forces = {
            "clarity": float,
            "coherence": float,
            "emotion": float,
            "symbolic": float,
            "memory": float,
            "chaos": float
        }

        Returns a stability score between 0 and 1.
        """

        # Chaos reduces stability, others increase it
        positive = (
            forces.get("clarity", 0) +
            forces.get("coherence", 0) +
            forces.get("emotion", 0) +
            forces.get("symbolic", 0) +
            forces.get("memory", 0)
        ) / 5.0

        chaos = forces.get("chaos", 0)

        # Stability is positive forces minus chaos influence
        stability = max(0.0, min(1.0, positive * (1 - chaos)))

        return stability

    def evaluate(self, forces):
        """
        Returns one of:
        - "ACCEPT"
        - "NOT_YET"
        - "UNFORMED"
        """

        stability = self.compute_stability(forces)

        if stability >= self.accept_threshold:
            return "ACCEPT", stability

        if stability >= self.not_yet_threshold:
            return "NOT_YET", stability

        return "UNFORMED", stability
