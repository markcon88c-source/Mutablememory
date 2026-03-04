class WorldViewerOrgan:
    """
    Cathedral World Viewer Organ.
    Captures a snapshot of world-related fields for viewer layers.
    """

    def __init__(self):
        self.last_snapshot = {}

    def tick(self, iteration, packet):
        if packet is None:
            packet = {}

        world_state = packet.get("world", {})
        gravity_state = packet.get("gravity", {})
        idea_state = packet.get("idea", {})

        snapshot = {
            "iteration": iteration,
            "world": world_state,
            "gravity": gravity_state,
            "idea": idea_state
        }

        self.last_snapshot = snapshot
        packet["world_viewer"] = snapshot

        return packet
