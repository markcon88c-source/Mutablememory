# ============================================================
# 🎉 CHARACTER BIRTH VIEWER — MYTHIC · CINEMATIC · PARTY MODE 🎉
# ============================================================

class BirthViewer:
    """
    A ceremonial viewer that witnesses the emergence of a new
    character within the Cathedral creature. Expressive, mythic,
    celebratory, and fully orchestrator‑compatible.
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None
        self.birth_count = 0

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if isinstance(packet, dict):
            self.last_packet = packet
            self.birth_count += 1

    # --------------------------------------------------------
    # INTERNAL RENDER (string)
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_packet:
            return (
                "=== 🎉 CHARACTER BIRTH VIEWER 🎉 ===\n"
                "(awaiting first emergence… ✨)"
            )

        name = self.last_packet.get("name", "Unnamed")
        traits = self.last_packet.get("traits", {})
        origin = self.last_packet.get("origin", "Unknown Source")
        pulse = self.last_packet.get("pulse", None)

        lines = []
        lines.append("=== 🎉 CHARACTER BIRTH VIEWER 🎉 ===")
        lines.append(f"🌟 Birth Event #{self.birth_count} 🌟")
        lines.append(f"🧬 Name: {name}")
        lines.append(f"🏛️ Origin: {origin}")

        if traits:
            lines.append("💠 Traits:")
            for k, v in traits.items():
                lines.append(f"   • {k}: {v}")

        if pulse is not None:
            lines.append(f"💓 Pulse Signature: {pulse}")

        lines.append("🎊 A new presence enters the Cathedral… 🎊")

        return "\n".join(lines)

    # --------------------------------------------------------
    # ORCHESTRATOR-COMPATIBLE RENDER(packet)
    # --------------------------------------------------------
    def render(self, packet):
        """
        The orchestrator passes a packet, but this viewer uses
        self.last_packet from receive_packet(). We ignore the
        incoming packet and render the stored birth frame.
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
            source="character_birth_viewer",
            channel="visual",
            kind="character_birth_view",
            payload={
                "type": "character_birth_view",
                "text": text
            }
        )
