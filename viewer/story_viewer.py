# ============================================================
# STORY VIEWER — CATHEDRAL NARRATIVE PHYSICS EDITION
# ============================================================
# Reads metabolized packets and extracts:
#   - Storyline (word chain)
#   - Narrative Anchor (strongest-force word)
#   - Force-field readout (spark / storm / clarity)
#   - Motif emergence
#   - Story gravity (coherence pressure)
#
# Fully compatible with the ViewerOrchestrator.
# ============================================================

class StoryViewer:
    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # Orchestrator entrypoint
    # --------------------------------------------------------
    def render(self, packet):
        """
        packet: list of metabolized word-packets
        Returns list of lines for orchestrator.
        """
        if not isinstance(packet, list) or not packet:
            return [
                "📖 STORY VIEW",
                "──────────────────────────────────────────────",
                "(no story packets yet)"
            ]

        self.last_packet = packet

        # Extract words
        words = [p.get("word", "") for p in packet if isinstance(p, dict)]
        storyline = " ".join(words).strip()

        # Find strongest-force packet
        strongest = None
        max_force = -1.0

        for p in packet:
            if not isinstance(p, dict):
                continue
            fs = p.get("force_score", 0.0)
            if fs > max_force:
                strongest = p
                max_force = fs

        # Extract forces
        if strongest:
            anchor_word = strongest.get("word", "")
            forces = strongest.get("forces", {})
            spark = forces.get("spark", 0.0)
            storm = forces.get("storm", 0.0)
            clarity = forces.get("clarity", 0.0)
        else:
            anchor_word = ""
            spark = storm = clarity = 0.0

        # Story gravity = coherence of force distribution
        story_gravity = max(0.0, min(1.0, (clarity + spark) - storm))

        # Motif emergence (very simple heuristic)
        motif = ""
        if clarity > 0.6:
            motif = "✨ Clarity Motif Emerging"
        elif storm > 0.6:
            motif = "🌩️ Storm Motif Emerging"
        elif spark > 0.6:
            motif = "🔥 Spark Motif Emerging"

        # Build output
        lines = []
        lines.append("📖 STORY VIEW")
        lines.append("──────────────────────────────────────────────")
        lines.append(f"Storyline: {storyline if storyline else '(empty)'}")
        lines.append("")
        lines.append(f"Narrative Anchor: {anchor_word}")
        lines.append(f"  Spark:   {spark:.2f}")
        lines.append(f"  Storm:   {storm:.2f}")
        lines.append(f"  Clarity: {clarity:.2f}")
        lines.append("")
        lines.append(f"Story Gravity: {story_gravity:.2f}")
        if motif:
            lines.append(motif)
        lines.append("──────────────────────────────────────────────")

        return lines

