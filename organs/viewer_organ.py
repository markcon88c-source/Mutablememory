# ============================================================
# VIEWER ORGAN — CATHEDRAL VIEWER RENDERING NODE (ORGAN LAYER)
# ============================================================

class ViewerOrgan:
    """
    Viewer organ wired as part of the Cathedral organ stack.
    Old metabolism used tick(self); Cathedral uses tick(self, creature)
    and returns packets instead of pushing directly.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_frame = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        source = packet.get("source", "unknown")
        kind = packet.get("kind", "unknown")
        payload = packet.get("payload", {})

        self.last_frame = {
            "source": source,
            "kind": kind,
            "payload": payload
        }

    # ========================================================
    # NEW PHYSIOLOGY — your real logic (renamed)
    # ========================================================
    def tick_core(self, creature):
        """
        Cathedral metabolism: return a viewer frame packet.
        """
        if not self.last_frame:
            return None

        return {
            "source": "viewer_organ",
            "channel": "viewer",
            "kind": "frame",
            "payload": self.last_frame,
        }

    # ========================================================
    # LEGACY COMPATIBILITY WRAPPER
    # CreatureCathedral calls organ.tick() with NO arguments
    # ========================================================
    def tick(self):
        return self.tick_core(self.creature)
