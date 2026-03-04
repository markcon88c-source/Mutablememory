# ============================================================
# CATHEDRAL SENTENCE VIEWER — MODERN REBUILD
# ============================================================
# Reads the unified packet from SentenceOrgan and renders:
#   - Word box
#   - Phonetic signature
#   - Phonetic graph (ASCII waveform)
#   - Pressure metrics
#   - Cluster / Oppose
#
# This is the foundation for the 21+ viewer suite.
# ============================================================

import math

class SentenceViewer:

    def __init__(self, creature):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # Utility: simple ASCII graph from phonetic vector
    # --------------------------------------------------------
    def graph_line(self, vec, width=40, height=8):
        if not vec:
            return ["(no phonetic vector)"]

        maxv = max(abs(v) for v in vec) or 1.0
        norm = [v / maxv for v in vec]

        step = max(1, len(norm) // width)
        samples = norm[::step][:width]

        rows = []
        for h in range(height, -1, -1):
            threshold = (h / height) * 1.0
            row = "".join("█" if abs(v) >= threshold else " " for v in samples)
            rows.append(row)
        return rows

    # --------------------------------------------------------
    # Utility: bar meter for pressure/drift/etc.
    # --------------------------------------------------------
    def bar(self, value, max_value=1.0, width=20):
        if value is None:
            return "(no data)"
        filled = int((value / max_value) * width)
        filled = max(0, min(width, filled))
        return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"

    # --------------------------------------------------------
    # Main display
    # --------------------------------------------------------
    def display(self, packet):
        self.last_packet = packet

        word = packet.get("word", "")
        sig = packet.get("phonetic_signature", "")
        pvec = packet.get("phonetic_vector", [])
        pressure = packet.get("pressure", {})
        cluster = packet.get("cluster", 0.0)
        oppose = packet.get("oppose", 0.0)

        lines = []

        lines.append("==================================================")
        lines.append(f" WORD: {word}")
        lines.append("==================================================")

        lines.append(f" PHONETIC: {sig}")

        lines.append("--------------------------------------------------")
        lines.append(" PHONETIC GRAPH:")
        for row in self.graph_line(pvec):
            lines.append(" " + row)

        lines.append("--------------------------------------------------")
        lines.append(" PRESSURE METRICS:")
        for k, v in pressure.items():
            lines.append(f"  {k:12s} {self.bar(v)}")

        lines.append("--------------------------------------------------")
        lines.append(f" CLUSTER: {cluster:.3f}   {self.bar(cluster)}")
        lines.append(f" OPPOSE : {oppose:.3f}   {self.bar(oppose)}")

        lines.append("==================================================")

        return "\n".join(lines)

    # --------------------------------------------------------
    # Orchestrator compatibility wrapper
    # --------------------------------------------------------
    def render(self, packet):
        text = self.display(packet)
        return text.split("\n")
