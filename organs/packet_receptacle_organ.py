# organs/packet_receptacle_organ.py

class PacketReceptacleOrgan:
    """
    A simple ignition socket that attaches to an organ and fires it
    whenever a packet is received.
    """

    def __init__(self, creature, target_organ, accepted_types=None):
        self.creature = creature
        self.target_organ = target_organ
        self.accepted_types = accepted_types or []  # e.g. ["sentence", "force", "command"]
        self.last_packet = None
        self.state = "OFF"  # OFF, WAITING, ON

    def handle_packet(self, packet):
        """
        Called by the universal bus or a direct connection.
        Stores the packet and prepares to ignite.
        """
        ptype = packet.get("type")

        # If we have filters, ignore other packets
        if self.accepted_types and ptype not in self.accepted_types:
            return

        self.last_packet = packet
        self.state = "WAITING"

        # Immediately ignite
        self.ignite()

    def ignite(self):
        """
        Fires the target organ's step() with the last packet.
        """
        if not self.last_packet:
            return

        try:
            self.target_organ.step(self.last_packet)
            self.state = "ON"
        except Exception as e:
            print(f"[PacketReceptacle] Error firing organ: {e}")
            self.state = "ERROR"
