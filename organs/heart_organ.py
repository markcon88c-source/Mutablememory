# ============================================================
# HEART ORGAN — Cathedral Core Pulse Generator
# ============================================================

from organs.base_organ import BaseOrgan

class HeartOrgan(BaseOrgan):
    """
    The central rhythmic driver of the Cathedral creature.
    Emits heartbeat packets and maintains cycle count.
    """

    def __init__(self, creature):
        super().__init__(creature)
        self.cycle = 0
        self.last_packet = None

    def receive(self, packet):
        # Store last received packet for diagnostics
        self.last_packet = packet

    def tick(self):
        # Increment heartbeat cycle
        self.cycle += 1

        # Emit heartbeat packet into the bloodstream
        self.creature.bus.emit(
            source="HeartOrgan",
            channel="heart",
            kind="heartbeat",
            payload={"cycle": self.cycle},
        )

    def snapshot(self):
        return {
            "cycle": self.cycle,
            "last_packet": self.last_packet,
        }
