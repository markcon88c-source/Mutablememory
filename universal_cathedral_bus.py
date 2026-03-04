# ============================================================
# UNIVERSAL CATHEDRAL BUS
# Packet-based metabolic bus for the Cathedral Creature
# ============================================================

import time


class UniversalCathedralBus:
    def __init__(self, creature):
        self.creature = creature

        # Organ registry (organs register themselves here)
        self.registry = {}

        # Packet log (viewers read from here)
        self.packets = []

        # Snapshot cache (viewers read this)
        self._snapshot = {
            "packets": self.packets,
            "registry": self.registry
        }

    # --------------------------------------------------------
    # Organ registration (Creature calls this)
    # --------------------------------------------------------
    def register(self, organ):
        """
        Register an organ into the Cathedral bus registry.
        Creature expects this method to exist.
        """
        name = organ.__class__.__name__
        self.registry[name] = organ

    # --------------------------------------------------------
    # Emit packets into the bus
    # --------------------------------------------------------
    def emit(self, packet):
        """
        Emit a metabolic packet into the Cathedral bus.
        Packets are dictionaries produced by organs.
        """
        if packet is None:
            return

        # Attach timestamp
        packet["_timestamp"] = time.time()

        # Store packet
        self.packets.append(packet)

    # --------------------------------------------------------
    # Snapshot for viewers
    # --------------------------------------------------------
    def snapshot(self):
        """
        Return a stable snapshot of the bus state.
        Viewers use this to render.
        """
        return self._snapshot

    # --------------------------------------------------------
    # Optional: clear packets (not used by Creature)
    # --------------------------------------------------------
    def clear(self):
        self.packets.clear()
