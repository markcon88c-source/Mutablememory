# organs/force_normalizer.py

class ForceNormalizer:
    """
    ForceNormalizer
    ----------------
    Normalizes packet force values so downstream organs and
    cathedral viewers never receive runaway or invalid forces.
    """

    def __init__(self, creature):
        self.creature = creature

    # ---------------------------------------------------------
    # MAIN METABOLIC ENTRYPOINT
    # ---------------------------------------------------------
    def run(self, packets):
        """
        Accepts a list of packets and returns a normalized list.
        Each packet must contain a 'force' field.
        """

        if not packets:
            return []

        normalized = []
        for p in packets:
            force = p.get("force", 1.0)

            # Clamp to safe range
            if force < 0.0:
                force = 0.0
            elif force > 1.0:
                force = 1.0

            # Build normalized packet
            normalized.append({
                **p,
                "force": force,
            })

        return normalized
