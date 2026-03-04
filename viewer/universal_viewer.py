# ============================================================
# UNIVERSAL VIEWER — ORCHESTRATOR EDITION
# ============================================================

class UniversalViewer:
    """
    Displays any packet routed through the universal bus.
    Fully compatible with the ViewerOrchestrator.
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

        # Accept any universal packet
        if packet.get("channel") == "universal" or packet.get("kind") == "universal":
            self.last_packet = packet.get("payload", packet)

    # --------------------------------------------------------
    # INTERNAL RENDER (string)
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_packet:
            return "=== UNIVERSAL VIEWER ===\n(no universal packets yet)"

        lines = []
        lines.append("=== UNIVERSAL VIEWER ===")
        lines.append("Universal packet received:")

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
        incoming packet and render the stored universal frame.
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
            source="universal_viewer",
            channel="visual",
            kind="universal_view",
            payload={
                "type": "universal_view",
                "text": text
            }
        )
