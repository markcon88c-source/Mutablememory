# ============================================================
# CATHEDRAL RECEPTACLE — FINAL METABOLIC SINK
# ============================================================

class CathedralReceptacle:
    """
    The Receptacle is the final metabolic sink in the Cathedral creature.
    It receives packets from the injector or universal bus and stores the
    most recent one. On each heartbeat, it returns a normalized packet
    for downstream viewers or debugging layers.

    Old metabolism used tick(self) and direct bus emission.
    Cathedral metabolism uses tick(self, creature) and returns packets.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # RECEIVE PACKET — called by injector or bus
    # --------------------------------------------------------
    def receive_packet(self, packet):
        self.last_packet = packet

    # ========================================================
    # NEW PHYSIOLOGY — your real logic (renamed)
    # ========================================================
    def tick_core(self, creature):
        """
        Cathedral metabolism:
        - creature calls: receptacle.tick(self)
        - we return the last received packet (or None)
        - injector/bus/viewer orchestrator decide what to do with it
        """
        if self.last_packet is None:
            return None

        return {
            "source": "receptacle",
            "channel": "metabolism",
            "kind": "sink",
            "payload": self.last_packet,
        }

    # ========================================================
    # LEGACY COMPATIBILITY WRAPPER
    # CreatureCathedral calls receptacle.tick() with NO arguments
    # ========================================================
    def tick(self):
        return self.tick_core(self.creature)
