# ============================================================
# WORLD VIEWER — ORCHESTRATOR EDITION
# ============================================================

class WorldViewer:
    """
    Minimal but fully orchestrator‑compatible WorldViewer.
    Displays the last world packet received.
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if not isinstance(packet, dict):
            return

        # Accept packets with channel='world' or type='world'
        if packet.get("channel") == "world" or packet.get("type") == "world":
            self.last_packet = packet.get("payload", packet)

    # --------------------------------------------------------
    # INTERNAL RENDER (string)
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_packet:
            return "=== WORLD VIEWER ===\n(no world packets yet)"

        lines = []
        lines.append("=== WORLD VIEWER ===")
        lines.append("World packet received:")

        pkt = self.last_packet
        if isinstance(pkt, dict):
            for k, v in pkt.items():
                lines.append(f" - {k}: {v}")
        else:
            lines.append(f" - {pkt!r}")

        return "\n".join(lines)

    # --------------------------------------------------------
    # ORCHESTRATOR-COMPATIBLE RENDER(packet)
    # --------------------------------------------------------
    def render(self, packet):
        """
        The orchestrator passes a packet, but this viewer uses
        self.last_packet from receive_packet(). We ignore the
        incoming packet and render the stored world frame.
        """
        text = self._render_internal()
        return text.split("\n")

    # --------------------------------------------------------
    # TICK — emit frame to the universal bus
    # --------------------------------------------------------
    def tick(self):
        text = self._render_internal()
        if not text:
            return

        self.creature.universal_bus.emit(
            source="world_viewer",
            channel="visual",
            kind="world_view",
            payload={
                "type": "world_view",
                "text": text
            }
        )
