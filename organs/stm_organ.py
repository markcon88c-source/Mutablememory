# organs/stm_organ.py

class STMOrgan:
    """
    Minimal STM organ that provides metrics required by IntegrityViewer.
    """

    def __init__(self, creature):
        self.creature = creature

        # Minimal internal state
        self.word_count = 0
        self.density = 0.0
        self.unresolved_hooks = 0
        self.unresolved_fragments = 0
        self.abandoned_clusters = 0

        self.drift_summary = {
            "avg": 0.0,
            "last": 0.0,
        }

        self.pressure_summary = {
            "avg": {},
            "last": {},
        }

    def step(self, packet):
        """
        Update minimal STM state from packet.
        """
        if packet and isinstance(packet, dict):
            word = packet.get("word")
            if word:
                self.word_count += 1
                self.density = min(1.0, self.word_count / 100)

        return packet

    def get_metrics(self):
        """
        Return the exact structure IntegrityViewer expects.
        """
        return {
            "word_count": self.word_count,
            "density": self.density,
            "unresolved_hooks": self.unresolved_hooks,
            "unresolved_fragments": self.unresolved_fragments,
            "abandoned_clusters": self.abandoned_clusters,
            "drift_summary": self.drift_summary,
            "pressure_summary": self.pressure_summary,
        }
