# ============================================================
# PACKET BUS ORGAN — Cathedral Edition
# ------------------------------------------------------------
# Routes packets to any organ that implements handle_bus_packet().
# ============================================================

class PacketBusOrgan:
    """
    Central packet router. Any organ that wants to receive packets
    implements handle_bus_packet(packet).
    """

    def __init__(self, creature):
        self.creature = creature

    # --------------------------------------------------------
    # STEP — required by Creature heartbeat
    # --------------------------------------------------------
    def step(self, packet):
        """
        Called each heartbeat with the packet produced by the
        previous organ. Distributes it to all organs that
        implement handle_bus_packet().
        """

        if packet is None:
            return None

        for organ in self.creature.organs.values():
            handler = getattr(organ, "handle_bus_packet", None)
            if callable(handler):
                handler(packet)

        # Bus does not transform packets; it just routes them.
        return packet
