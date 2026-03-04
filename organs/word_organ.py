class WordOrgan:
    """
    WordOrgan:
    - Receives heart meaning
    - Computes polarity from cluster
    - Initializes meaning_strength, exposure, resonance
    - Produces memory packets for STMOrgan
    """

    def __init__(self):
        pass

    def compute_polarity(self, cluster):
        u = cluster.count("U")
        w = cluster.count("W")
        return (u - w) / max(1, len(cluster))

    def prepare_memory_packet(self, heart_state):
        if not isinstance(heart_state, dict):
            return None

        cluster = heart_state.get("cluster")
        meaning = heart_state.get("meaning", {})

        word = meaning.get("word")
        concept = meaning.get("concept")

        if not word:
            return None

        polarity = self.compute_polarity(cluster)

        packet = {
            "word": word,
            "concept": concept,
            "cluster": cluster,
            "polarity": polarity,
            "meaning_strength": 0.10,
            "exposure": 1,
            "resonance": 0.0,
            "level": 0,
            "gate": 1
        }

        return packet
