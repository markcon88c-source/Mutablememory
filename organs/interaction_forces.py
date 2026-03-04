# INTERACTION FORCES — CATHEDRAL EDITION
# Computes interaction-based force adjustments between packets.
# No self-imports. No circular dependencies. Fully self-contained.

class InteractionForces:
    def __init__(self, creature=None):
        self.creature = creature
        self.interaction_energy = 0.0
        self.decay = 0.90

    def tick(self, packets=None):
        if packets is None:
            packets = getattr(self.creature, "last_packets", [])

        # Decay old energy
        self.interaction_energy *= self.decay

        # Pairwise interactions
        for i in range(len(packets)):
            p1 = packets[i]
            if not isinstance(p1, dict):
                continue

            fp1 = p1.get("force_profile")
            if not fp1:
                continue

            for j in range(i + 1, len(packets)):
                p2 = packets[j]
                if not isinstance(p2, dict):
                    continue

                fp2 = p2.get("force_profile")
                if not fp2:
                    continue

                # Compute simple interaction metric
                spark_diff = abs(fp1.get("spark", 0.0) - fp2.get("spark", 0.0))
                drift_diff = abs(fp1.get("drift", 0.0) - fp2.get("drift", 0.0))
                echo_diff = abs(fp1.get("echo", 0.0) - fp2.get("echo", 0.0))

                # Interaction energy increases when forces differ
                self.interaction_energy += (
                    (spark_diff * 0.3) +
                    (drift_diff * 0.2) +
                    (echo_diff * 0.1)
                )

        # Clamp
        if self.interaction_energy < 0:
            self.interaction_energy = 0.0
        if self.interaction_energy > 100:
            self.interaction_energy = 100.0

        # Expose to creature state
        if self.creature:
            self.creature.state["interaction_energy"] = self.interaction_energy

    def get_energy(self):
        return self.interaction_energy
