# organs/idea.py

from decimal import Decimal


class Idea:
    """
    Core idea object used by WorldIdeaOrgan.
    Stores:
      • id
      • words
      • block_id
      • signature (x, y, z)
      • age
      • gravity
      • forces (strength, drift, resonance, opposition, clustering)
      • attached_metrics
    """
    _id_counter = 1

    def __init__(self, words, block_id, signature):
        self.id = Idea._id_counter
        Idea._id_counter += 1

        self.words = words
        self.block_id = block_id
        self.signature = signature  # (x, y, z) floats or Decimals

        self.age = 0
        self.gravity = Decimal("0.0")
        self.forces = {}
        self.attached_metrics = []

    def compute_gravity(self, metric_vector):
        """
        Compute gravitational pull toward story metrics.
        metric_vector = { "Plot": 0.12, "Theme": 0.18, ... }
        """
        s, d, r = self.signature

        mapping = {
            "Plot": abs(s),
            "Theme": abs(d),
            "Symbol": abs(r),
            "Tone": (s + r) / 2,
            "Character": abs(d * r),
            "Conflict": abs(s - r),
            "Myth": abs(s + d + r),
            "Setting": abs(d),
        }

        gravity = Decimal("0.0")
        for k, v in metric_vector.items():
            gravity += Decimal(str(mapping[k])) * Decimal(str(v))

        self.gravity = gravity
