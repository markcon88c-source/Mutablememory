class PacketTraceOrgan:
    """
    Records which organs received the last packet.
    Produces a YES/NO map for the diagnostic viewer.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_packet = None
        self.trace = {}

    def handle_bus_packet(self, packet):
        """
        Called by the Universal Bus for every packet.
        """
        self.last_packet = packet
        self.trace = {}

        # Mark all organs as NO initially
        for name in self.creature.organs.keys():
            self.trace[name] = "NO"

        # Any viewer or organ tapped to the bus that receives this packet
        # will mark YES through this method
        for name, organ in self.creature.organs.items():
            try:
                # If the organ has handle_bus_packet, assume it received it
                if hasattr(organ, "handle_bus_packet"):
                    self.trace[name] = "YES"
            except Exception:
                pass

    def snapshot(self):
        return {
            "packet": self.last_packet,
            "trace": self.trace
        }
