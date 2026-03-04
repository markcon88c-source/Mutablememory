class UniversalBus:
    """
    The Universal Bus is the bloodstream of the creature.
    Organs push packets into it, and the Injector pulls them out.
    """

    def __init__(self):
        self._packets = []
        self._receptacles = []

    def register_receptacle(self, receptacle):
        """Register an organ or viewer inbox."""
        self._receptacles.append(receptacle)

    def push(self, packet):
        """Organs push packets into the bus."""
        if packet is not None:
            self._packets.append(packet)

    def push_many(self, packets):
        """Push multiple packets at once."""
        if packets:
            self._packets.extend(packets)

    def collect_packets(self):
        """
        Return all packets currently in the bus and clear it.
        The Injector will deliver these to the Receptacle.
        """
        packets = self._packets
        self._packets = []
        return packets
