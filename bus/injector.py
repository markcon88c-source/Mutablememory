# ============================================================
# CATHEDRAL INJECTOR — forwards packets into the Universal Bus
# ============================================================

class Injector:
    """
    Receives packets from the creature and forwards them into the
    UniversalBus so subscribers can receive them.
    """

    def __init__(self, bus):
        self.bus = bus

    def push(self, packet):
        """
        Called by the creature heartbeat. Any organ that emits a packet
        should ultimately flow through here.
        """
        if packet is not None:
            self.bus.emit(packet)

    def deliver(self):
        """
        Called by the creature heartbeat to retrieve packets that the
        bus emitted this frame.
        """
        if hasattr(self.bus, "drain"):
            return self.bus.drain()
        return []
