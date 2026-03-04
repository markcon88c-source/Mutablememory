# ============================================================
# DIAGNOSTIC VIEWER — Cathedral / Experimental-Wall Hybrid
# ============================================================

class DiagnosticViewer:
    def __init__(self, creature=None):
        # Creature is optional; some architectures pass it, some don't
        self.creature = creature
        self.last_packet = None

    def render(self, packet, snapshot=None):
        """
        packet: latest packet (may be None)
        snapshot: full bus snapshot (dict)
        """

        # Provide a safe empty snapshot if none was passed
        if snapshot is None:
            snapshot = {
                "registry": [],
                "organs": [],
                "packets": [],
                "last_broadcast": None,
                "message_log": []
            }

        registry = snapshot.get("registry", [])
        organs = snapshot.get("organs", [])
        packets = snapshot.get("packets", [])
        last_broadcast = snapshot.get("last_broadcast", None)
        message_log = snapshot.get("message_log", [])

        out = []
        out.append("=== DIAGNOSTIC VIEWER ===")
        out.append("")

        # Registry
        out.append("Registered Organs:")
        for name in registry:
            out.append(f" - {name}")
        out.append("")

        # Organ list
        out.append("Organ Keys:")
        for name in organs:
            out.append(f" - {name}")
        out.append("")

        # Last broadcast
        out.append("Last Broadcast Packet:")
        if last_broadcast:
            out.append(f" {last_broadcast}")
        else:
            out.append(" (none)")
        out.append("")

        # Packet count
        out.append(f"Total Packets: {len(packets)}")
        out.append("")

        # Message log (list, not dict)
        out.append("Recent Messages:")
        if message_log:
            for msg in message_log[-5:]:
                out.append(f" - {msg}")
        else:
            out.append(" (no messages)")
        out.append("")

        return out
