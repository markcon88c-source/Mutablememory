# NARRATIVE GRAVITY WELL ORGAN — CATHEDRAL EDITION
# Provides the global narrative gravity vector that shapes story drift.

class NarrativeGravityWellOrgan:
    def __init__(self, creature):
        self.creature = creature

        # Core gravity components
        self.gravity = {
            "coherence_pull": 0.0,
            "motif_pull": 0.0,
            "identity_pull": 0.0,
            "chaos_pull": 0.0,
        }

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.gravity:
                self.gravity[k] = v

    def gravity_vector(self):
        return [
            self.gravity["coherence_pull"],
            self.gravity["motif_pull"],
            self.gravity["identity_pull"],
            self.gravity["chaos_pull"],
        ]

    def tick(self):
        return self.gravity_vector()
