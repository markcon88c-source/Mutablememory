# organs/alert_pressure_organ.py
# ============================================================
# ALERT PRESSURE ORGAN — computes alert level from packets
# ============================================================

class AlertPressureOrgan:
    """
    Computes alert pressure based on packet flow.
    Produces:
        - alert_value (float)
    """

    def __init__(self, creature):
        self.creature = creature

    def metabolize(self, packets):
        if not packets:
            return {"alert_value": 0.0}

        alert = 0.0

        # Look for alert packets or semantic hints
        for p in packets:
            ptype = p.get("type")

            # Direct alert packet
            if ptype == "alert":
                alert = p.get("value", alert)

            # Semantic tags can influence alert pressure
            if "tag" in p:
                tag = p["tag"]
                if tag == "danger":
                    alert += 0.2
                elif tag == "safe":
                    alert -= 0.1

        # Clamp alert to [0.0, 1.0]
        alert = max(0.0, min(1.0, alert))

        return {"alert_value": alert}
