# organs/force_organ.py
# ============================================================
# FORCE ORGAN — computes spark, drift-force, and echo energy
# ============================================================

class ForceOrgan:
    """
    Computes force metrics from packets and meaning metadata.
    Produces a dict with:
        - spark
        - drift_force
        - echo
    """

    def __init__(self, creature):
        self.creature = creature

    def metabolize(self, packets, meaning_meta):
        if not packets:
            return {
                "force_output": {
                    "spark": 0.0,
                    "drift": 0.0,
                    "echo": 0.0
                }
            }

        # Basic energy model
        spark = 0.0
        drift_force = 0.0
        echo = 0.0

        # Meaning meta may contain math blocks or semantic energy
        if meaning_meta:
            block = meaning_meta.get("math_block", {})
            spark = block.get("energy", 0.0)
            drift_force = block.get("drift", 0.0)
            echo = block.get("echo", 0.0)

        # Clamp values
        spark = max(0.0, min(1.0, spark))
        drift_force = max(-1.0, min(1.0, drift_force))
        echo = max(0.0, min(1.0, echo))

        return {
            "force_output": {
                "spark": spark,
                "drift": drift_force,
                "echo": echo
            }
        }
