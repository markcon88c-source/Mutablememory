# ============================================================
# MEANING ORGAN — LEXICAL → SEMANTIC (+ PROTO COMPATIBILITY)
# ============================================================

class MeaningOrgan:
    """
    Converts lexical packets into semantic packets enriched with
    proto-sentence compatible fields. This allows downstream organs
    (ProtoSentenceOrgan, SentenceOrgan) to treat semantic packets
    as valid sentence precursors.
    """

    def __init__(self, creature):
        self.creature = creature
        self.bus = creature.bus
        self.last_packet = None

    # --------------------------------------------------------
    # Bus interface
    # --------------------------------------------------------
    def receive(self, packet):
        self.last_packet = packet

    # --------------------------------------------------------
    # Metabolic step
    # --------------------------------------------------------
    def tick(self):
        packet = self.last_packet
        if not isinstance(packet, dict):
            return

        if packet.get("type") != "lexical":
            return

        lexical_data = packet.get("lexical", {})
        word = lexical_data.get("word")
        if not word:
            return

        # Basic semantic scaffold (expand as needed)
        meaning_data = {
            "gravity": 0.2,
            "forces": {},
            "identity": packet.get("identity", {}),
            "emotion": packet.get("emotion", {}),
            "story": packet.get("story", {}),
            "world": packet.get("world", {}),
        }

        semantic_packet = {
            "type": "semantic",
            "channel": "semantic",
            "source": "meaning",

            # Core semantic content
            "meaning": meaning_data,
            "lexical": lexical_data,

            # Proto-sentence compatibility
            "proto_tokens": [word],
            "proto_language": word,

            # Unified fields
            "anchor": word,
            "gravity": meaning_data.get("gravity", 0.2),
            "forces": meaning_data.get("forces", {}),
        }

        self.bus.emit(semantic_packet)
        self.last_packet = None
