# ============================================================
# LANGUAGE ORGAN — PACKET NORMALIZATION + WORD CHANNELING
# ============================================================

class LanguageOrgan:
    """
    Normalizes packets coming from VocabularyOrgan and routes
    lexical/identity/faction words into a unified packet format.
    """

    def __init__(self, creature):
        self.creature = creature

    # --------------------------------------------------------
    # Normalize incoming packets
    # --------------------------------------------------------
    def normalize(self, packet):
        """
        Convert vocabulary frames or emitted words into a standard
        packet format for downstream organs.
        """

        if not isinstance(packet, dict):
            return packet

        # Vocabulary frame passthrough
        if packet.get("type") == "vocabulary_frame":
            return packet

        # Legacy vocabulary emissions
        kind = packet.get("kind")
        payload = packet.get("payload", {})

        if kind == "lexical_word":
            return {
                "type": "word",
                "class": "lexical",
                "word": payload.get("word")
            }

        if kind == "identity_word":
            return {
                "type": "word",
                "class": "identity",
                "word": payload.get("word")
            }

        if kind == "faction_word":
            return {
                "type": "word",
                "class": "faction",
                "word": payload.get("word")
            }

        return packet

    # --------------------------------------------------------
    # Metabolic step — required by Creature pipeline
    # --------------------------------------------------------
    def step(self, packet):
        """
        LanguageOrgan transforms vocabulary emissions into a unified
        packet format. If nothing matches, the packet passes through.
        """
        return self.normalize(packet)
