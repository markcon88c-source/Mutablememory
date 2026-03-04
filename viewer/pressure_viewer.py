# ============================================================
# 🎨 PRESSURE VIEWER — ORCHESTRATOR EDITION
# Displays symbolic → spark influence and all sub-forces.
# ============================================================

class PressureViewer:
    def __init__(self, creature):
        self.creature = creature

    def render(self, packets):
        """
        Render symbolic pressure and all known forces.
        Accepts packets from PacketBusOrgan.
        Returns a list of lines for the orchestrator.
        """

        # ---------------------------------------------------------
        # Extract the sentence packet
        # ---------------------------------------------------------
        sentence_packets = [
            p for p in packets
            if isinstance(p, dict) and p.get("type") == "sentence"
        ]

        if sentence_packets:
            forces = sentence_packets[0].get("forces", {})
        else:
            forces = {}

        # ---------------------------------------------------------
        # Extract key symbolic values
        # ---------------------------------------------------------
        symbolic = forces.get("symbolic", 0.0)
        spark_effective = forces.get("spark_effective", 0.0)
        spark_after = forces.get("spark_after", 0.0)

        # ---------------------------------------------------------
        # Build lines instead of printing
        # ---------------------------------------------------------
        lines = []
        lines.append("=== 🔮 SYMBOLIC PRESSURE VIEW ===")
        lines.append(f"🧠 Symbolic: {symbolic:.3f}")
        lines.append(f"✨ Spark Effective: {spark_effective:.3f}")
        lines.append(f"🌓 Spark After Symbolic: {spark_after:.3f}")
        lines.append("")
        lines.append("🌱 Sub‑forces:")
        lines.append("=================================")

        # Print all forces, sorted for stability
        for k in sorted(forces.keys()):
            lines.append(f"{k}: {forces[k]}")

        lines.append("")
        return lines
