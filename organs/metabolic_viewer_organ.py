class MetabolicViewerOrgan:
    """
    Cathedral Metabolic Viewer Organ.
    Collects a snapshot of the packet each heartbeat for viewer layers.
    """

    def __init__(self):
        self.last_snapshot = {}

    def tick(self, iteration, packet):
        if packet is None:
            packet = {}

        # store a shallow snapshot for viewers
        self.last_snapshot = {
            "iteration": iteration,
            "keys": list(packet.keys())
        }

        packet["metabolic_viewer"] = self.last_snapshot
        return packet
