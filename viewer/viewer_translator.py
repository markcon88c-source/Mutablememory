# ============================================================
# VIEWER TRANSLATOR — CATHEDRAL SAFE NORMALIZER
# ============================================================

class ViewerTranslator:
    """
    The ViewerTranslator converts any incoming packet into a
    normalized dict for the viewer orchestrator. It must be
    tolerant of None, lists, malformed packets, and legacy
    formats. The viewer layer must never crash.
    """

    def __init__(self, creature):
        # Creature reference kept for future use
        self.creature = creature

    def translate(self, packet):
        # --------------------------------------------------------
        # Handle None
        # --------------------------------------------------------
        if packet is None:
            return {
                "source": "translator",
                "kind": "noop",
                "payload": {}
            }

        # --------------------------------------------------------
        # Handle lists (take last element)
        # --------------------------------------------------------
        if isinstance(packet, list):
            if not packet:
                return {
                    "source": "translator",
                    "kind": "noop",
                    "payload": {}
                }
            packet = packet[-1]

        # --------------------------------------------------------
        # Handle non-dict packets
        # --------------------------------------------------------
        if not isinstance(packet, dict):
            return {
                "source": "translator",
                "kind": "invalid_packet",
                "payload": {
                    "raw": packet
                }
            }

        # --------------------------------------------------------
        # Normal dict packet — ensure required fields exist
        # --------------------------------------------------------
        normalized = {
            "source": packet.get("source", "unknown"),
            "channel": packet.get("channel", "unknown"),
            "kind": packet.get("kind", "unknown"),
            "payload": packet.get("payload", {})
        }

        # Ensure payload is a dict
        if not isinstance(normalized["payload"], dict):
            normalized["payload"] = {"raw": normalized["payload"]}

        return normalized
