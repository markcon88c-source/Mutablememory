# ============================================================
# UNIVERSAL BUS — unified, listener‑based, viewer‑compatible
# ============================================================

class UniversalBus:
    """
    Central Cathedral packet bus.
    - Organs emit packets into it.
    - Injector drains packets each heartbeat.
    - Viewers and organs may subscribe as listeners.
    - Includes legacy .registry for compatibility.
    """

    def __init__(self):
        # Heartbeat queue (Injector uses this)
        self.packets = []

        # Real‑time listeners (StoryOrgan, WorldOrgan, Viewers)
        self.listeners = []

        # Legacy compatibility for older viewers
        # Some viewers expect a dict-like registry
        self.registry = {}

    # --------------------------------------------------------
    # Register a listener (organ or viewer)
    # --------------------------------------------------------
    def register(self, listener):
        self.listeners.append(listener)

    # --------------------------------------------------------
    # Emit a packet into the bus
    # --------------------------------------------------------
    def emit(self, packet):
        # Add to heartbeat queue
        self.packets.append(packet)

        # Broadcast to listeners
        for listener in self.listeners:
            # New-style listener
            if hasattr(listener, "receive"):
                listener.receive(packet)

            # Legacy-style listener
            elif hasattr(listener, "on_packet"):
                listener.on_packet(packet)

    # --------------------------------------------------------
    # Drain packets for the creature heartbeat
    # --------------------------------------------------------
    def drain(self):
        out = list(self.packets)
        self.packets.clear()
        return out
