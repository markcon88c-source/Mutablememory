# symbolic_spark_organ.py
# ============================================================
# SYMBOLIC SPARK ORGAN
# Reads forces from the Force Bus and computes:
#   - symbolic pressure
#   - spark effective
#   - spark after symbolic
# Writes results into creature.lastmeta for viewers.
# ============================================================

from organs.base_organ import BaseOrgan

class SymbolicSparkOrgan(BaseOrgan):
    def __init__(self, creature):
        self.creature = creature
        self.lastmeta = {}

    def step(self):
        forces = getattr(self.creature, "forces", {})

        symbolic = float(forces.get("symbolic", 0.0))
        chaos = float(forces.get("chaos", 0.0))
        drift = float(forces.get("drift", 0.0))

        # Simple placeholder symbolic model
        spark_effective = symbolic - (chaos * 0.2) - (drift * 0.1)
        if spark_effective < 0:
            spark_effective = 0.0

        spark_after = spark_effective  # placeholder

        meta = {
            "symbolic": symbolic,
            "sparkeffective": spark_effective,
            "sparkafter": spark_after,
            "subforces": forces
        }

        self.lastmeta = meta
        self.creature.lastmeta = meta
