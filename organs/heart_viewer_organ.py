class HeartViewerOrgan:
    """
    Cathedral Heart Viewer Organ.
    Captures a simple snapshot of heart-related fields for viewer layers.
    """

    def __init__(self):
        self.last_snapshot = {}

    def tick(self, iteration, packet):
        if packet is None:
            packet = {}

        # capture any heart-related fields if present
        heart_state = packet.get("heart", {})
        pressure_state = packet.get("pressure", {})

        snapshot = {
            "iteration": iteration,
            "heart": heart_state,
            "pressure": pressure_state
        }

        self.last_snapshot = snapshot
        packet["heart_viewer"] = snapshot

        return packet
