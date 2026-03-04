# organs/stability_organ.py
# ============================================================
# STABILITY ORGAN — computes stability and stability zone
# ============================================================

class StabilityOrgan:
    """
    Computes overall stability from packet flow, drift, and alert pressure.
    Produces:
        - stability (0.0 to 1.0)
        - stability_zone ("RED", "YELLOW", "BLUE", "GREEN")
    """

    def __init__(self, creature):
        self.creature = creature

    def metabolize(self, packets):
        if not packets:
            return {
                "stability": 0.0,
                "stability_zone": "RED"
            }

        # Basic stability model:
        # More packets = more metabolic coherence
        # Drift and alert pressure reduce stability
        drift = 0.0
        alert = 0.0

        # Extract drift and alert from packets if present
        for p in packets:
            if p.get("type") == "drift":
                drift = p.get("value", 0.0)
            if p.get("type") == "alert":
                alert = p.get("value", 0.0)

        # Compute stability
        stability = 1.0 - (abs(drift) * 0.4 + alert * 0.6)
        stability = max(0.0, min(1.0, stability))

        # Determine zone
        if stability < 0.25:
            zone = "RED"
        elif stability < 0.5:
            zone = "YELLOW"
        elif stability < 0.75:
            zone = "BLUE"
        else:
            zone = "GREEN"

        return {
            "stability": stability,
            "stability_zone": zone
        }
