# ============================================================
# CATHEDRAL VIEWER — ORCHESTRATOR EDITION
# ============================================================

class CathedralViewer:
    """
    A minimal but orchestrator-safe Cathedral viewer.
    Displays the last cathedral packet in a clean list-of-lines
    format so the orchestrator can iterate safely.
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if isinstance(packet, dict):
            self.last_packet = packet

    # --------------------------------------------------------
    # INTERNAL RENDER (string)
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_packet:
            return "=== CATHEDRAL VIEWER ===\n(no cathedral packets yet)"

        lines = ["=== CATHEDRAL VIEWER ===", "Cathedral packet received:"]
        for k, v in self.last_packet.items():
            lines.append(f" - {k}: {v}")
        return "\n".join(lines)

    # --------------------------------------------------------
    # ORCHESTRATOR-COMPATIBLE RENDER(packet)
    # --------------------------------------------------------
    def render(self, packet):
        """
        The orchestrator passes a packet, but this viewer uses
        self.last_packet from receive_packet(). We ignore the
        incoming packet and render the stored cathedral frame.
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
            source="cathedral_viewer",
            channel="visual",
            kind="cathedral_view",
            payload={
                "type": "cathedral_view",
                "text": text
            }
        )
