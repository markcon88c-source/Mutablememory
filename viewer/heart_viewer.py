# ============================================================
# HEART VIEWER — ORCHESTRATOR EDITION
# ============================================================
# Displays the creature's heartbeat, pulse, emotional load,
# or any heart‑state packets emitted by organs.
# Fully compatible with the ViewerOrchestrator.
# ============================================================

class HeartViewer:
    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        """
        Accept packets with channel='heart' or type='heart'.
        Store the payload for rendering.
        """
        if not isinstance(packet, dict):
            return

        if packet.get("channel") == "heart" or packet.get("type") == "heart":
            self.last_packet = packet.get("payload", packet)

    # --------------------------------------------------------
    # INTERNAL RENDER (string)
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_packet:
            return "=== HEART VIEWER ===\n(no heart packets yet)"

        lines = []
        lines.append("=== HEART VIEWER ===")
        lines.append("Heart packet received:")

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
        incoming packet and render the stored heart frame.
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
            source="heart_viewer",
            channel="visual",
            kind="heart_view",
            payload={
                "type": "heart_view",
                "text": text
            }
        )
