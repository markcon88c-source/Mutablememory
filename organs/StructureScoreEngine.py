class StructureScoreEngine:
    def __init__(self):
        pass

    def compute_score(self, force_values, final_weights):
        """
        force_values: dict of floats
        final_weights: dict of floats

        Returns a float between 0.0 and 1.0
        """

        # Weighted sum of all forces
        total = 0.0
        weight_sum = 0.0

        for force, value in force_values.items():
            weight = final_weights.get(force, 0.0)
            total += value * weight
            weight_sum += weight

        # Avoid division by zero
        if weight_sum == 0:
            return 0.0

        # Normalize to 0.0 - 1.0
        score = total / weight_sum

        # Clamp to safe range
        score = max(0.0, min(1.0, score))

        return score

    def classify_score(self, score):
        """
        Returns a label for the score
        """

        if score >= 0.80:
            return "excellent"
        elif score >= 0.50:
            return "good"
        elif score >= 0.30:
            return "weak"
        else:
            return "failed"
