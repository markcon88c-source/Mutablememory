# organs/story_metrics_organ.py

class StoryMetricsOrgan:
    """
    StoryMetricsOrgan
    -----------------
    Adds narrative metrics to the metabolic meta dictionary.
    This organ is intentionally lightweight and heartbeat‑safe.
    """

    def __init__(self, creature):
        self.creature = creature

    # ---------------------------------------------------------
    # MAIN METABOLIC ENTRYPOINT
    # ---------------------------------------------------------
    def run(self, meta):
        """
        Accepts a meta dict and returns an enriched meta dict.
        """

        if not isinstance(meta, dict):
            meta = {}

        # Pull stability for simple narrative mapping
        stability = meta.get("stability", 0.0)

        # Simple narrative classification
        if stability < 0.30:
            story_type = "fragment"
            destiny = "collapse"
        elif stability < 0.60:
            story_type = "attempt"
            destiny = "uncertain"
        elif stability < 0.65:
            story_type = "coherent"
            destiny = "stable"
        else:
            story_type = "emergent"
            destiny = "growth"

        # Attach narrative metrics
        meta["story_type"] = story_type
        meta["story_destiny"] = destiny

        return meta
