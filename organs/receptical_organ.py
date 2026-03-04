class PacketReceptacleOrgan:
    """
    A universal intake socket that sits on an organ.
    The injector calls this to deliver packets.
    """

    def __init__(self, creature, target_organ, accepted_types=None):
        self.creature = creature
        self.target_organ = target_organ
        self.accepted_types = accepted_types  # None = accept all packet types
        self.last_packet = None

    def accept(self, packet):
        # Optional type filtering
        if self.accepted_types and packet.ptype not in self.accepted_types:
            return  # ignore packet

        # Store packet for debugging/viewers
        self.last_packet = packet

        # Ignite the organ
        return self.target_organ.accept_packet(packet)
