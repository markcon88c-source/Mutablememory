# organs/integrity_organ.py

class IntegrityOrgan:
    """
    IntegrityOrgan
    --------------
    Computes structural stability from packets.
    Produces the 'meta' dict consumed by cathedral viewers.
    """

    def __init__(self, creature):
        self.creature = creature

    # ---------------------------------------------------------
    # MAIN METABOLIC ENTRYPOINT
    # ---------------------------------------------------------
    def run(self, packets):
        """
        Accepts packets and returns a meta dictionary.
        """

        if not packets:
            return {
                "stability": 0.0,
                "zone": "RED",
                "emoji": "🔴",
                "rejected": [],
            }

        # Compute a simple stability score
        forces = [p.get("force", 0.0) for p in packets]
        avg_force = sum(forces) / len(forces)

        # Map stability to zone + emoji
        if avg_force < 0.30:
            zone = "RED"
            emoji = "🔴"
        elif avg_force < 0.60:
            zone = "YELLOW"
            emoji = "🟡"
        elif avg_force < 0.65:
            zone = "GREEN"
            emoji = "🟢"
        else:
            zone = "EMERALD"
            emoji = "💚"

        return {
            "stability": avg_force,
            "zone": zone,
            "emoji": emoji,
            "rejected": [],
        }
