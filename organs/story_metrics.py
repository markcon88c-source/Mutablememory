# STORY METRICS ORGAN — CATHEDRAL EDITION

class StoryMetricsOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.metrics = {
            "coherence": 0.0,
            "tension": 0.0,
            "momentum": 0.0,
            "novelty": 0.0,
        }

    def compute_metrics(self, creature):
        def safe_float(x):
            try:
                return float(x)
            except Exception:
                return 0.0

        state = getattr(creature, "state", {})

        coherence = safe_float(state.get("coherence", 0.0))
        tension = safe_float(state.get("tension", 0.0))
        momentum = safe_float(state.get("momentum", 0.0))
        novelty = safe_float(state.get("novelty", 0.0))

        self.metrics = {
            "coherence": coherence,
            "tension": tension,
            "momentum": momentum,
            "novelty": novelty,
        }

        return self.metrics

    def tick(self, creature):
        return self.compute_metrics(creature)

    # -----------------------------------------------------
    # GRAVITY VECTOR — REQUIRED BY WORLD IDEA ORGAN
    # -----------------------------------------------------
    def gravity_vector(self):
        """
        Returns a normalized 4D vector based on the story metrics.
        Safe even if metrics are missing or zero.
        """
        c = float(self.metrics.get("coherence", 0.0))
        t = float(self.metrics.get("tension", 0.0))
        m = float(self.metrics.get("momentum", 0.0))
        n = float(self.metrics.get("novelty", 0.0))

        mag = (c*c + t*t + m*m + n*n) ** 0.5
        if mag == 0:
            return (0.0, 0.0, 0.0, 0.0)

        return (c/mag, t/mag, m/mag, n/mag)
