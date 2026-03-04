# ============================================================
# GRAVITY VIEWER — PACKET MASS + DENSITY
# ============================================================

class GravityViewer:
    def __init__(self, creature):
        self.creature = creature

    def render(self, packets):
        if not packets:
            return ["[gravity] no packets"]

        packet = packets[-1]
        lines = []
        lines.append("=== GRAVITY VIEWER ===")

        mass = len(packet)
        density = sum(1 for v in packet.values() if v)

        lines.append(f"mass: {mass}")
        lines.append(f"density: {density}")
        lines.append(f"fields: {', '.join(packet.keys())}")

        if "sentence" in packet:
            lines.append(f"sentence: {packet['sentence']}")

        return lines
