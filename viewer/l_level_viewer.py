# ============================================================
# PHASE‑E L‑LEVEL VIEWER — VERTICAL METABOLIC L‑LEVELS
# Shows rise force, height attempts, collisions, clumping,
# turbulence, and proto‑clusters across the 11×17 STM waterfall.
# ============================================================

class LLevelViewer:
    """
    Phase‑E L‑Level Viewer.
    This viewer displays the vertical metabolic L‑Levels:
    the 11×17 waterfall where words and sentences attempt
    to rise, collide, clump, and form proto‑clusters.
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.frames = []   # store multiple L‑Level packets

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("channel") != "l_levels":
            return

        payload = packet.get("payload")
        if payload:
            self.frames.append(payload)

        # Keep last 17 frames (vertical waterfall)
        self.frames = self.frames[-17:]

    # --------------------------------------------------------
    # ANALYZE INTERACTIONS
    # --------------------------------------------------------
    def analyze(self):
        if len(self.frames) < 2:
            return [], [], [], [], []

        clumps = []
        collisions = []
        turbulence = []
        lifts = []
        ascenders = []

        for i in range(len(self.frames)):
            for j in range(i + 1, len(self.frames)):
                a = self.frames[i]
                b = self.frames[j]

                # Vertical distance
                vdist = abs(a.get("height_attempted", 0) - b.get("height_attempted", 0))

                # Horizontal drift difference
                drift = abs(a.get("drift", 0) - b.get("drift", 0))

                # Clumping (close vertical proximity)
                if vdist < 2:
                    clumps.append((a["id"], b["id"]))

                # Collision (same height, opposing drift)
                if vdist == 0 and a.get("drift", 0) * b.get("drift", 0) < 0:
                    collisions.append((a["id"], b["id"]))

                # Turbulence (rapid vertical divergence)
                if vdist > 5:
                    turbulence.append((a["id"], b["id"]))

                # Mutual lift (similar rise force)
                if abs(a.get("rise_force", 0) - b.get("rise_force", 0)) < 1:
                    lifts.append((a["id"], b["id"]))

        # Ascenders: strong upward motion
        for f in self.frames:
            if f.get("rise_force", 0) > 2 or f.get("height_attempted", 0) > 1:
                ascenders.append(f["id"])

        return clumps, collisions, turbulence, lifts, ascenders

    # --------------------------------------------------------
    # ORIGINAL RENDER (renamed)
    # --------------------------------------------------------
    def render_original(self):
        if not self.frames:
            return None

        clumps, collisions, turbulence, lifts, ascenders = self.analyze()

        def fmt(pairs, emoji):
            return "\n".join(f"  {emoji} {a} ↔ {b}" for a, b in pairs) if pairs else "  (none)"

        asc_text = "\n".join(f"  🐟 {sid} rising" for sid in ascenders) \
                   if ascenders else "  (none)"

        frame = f"""
===================== 🧗 PHASE‑E L‑LEVEL VIEWER 🧗 =====================

Active Entities: {len(self.frames)}

🐟 Ascenders (vertical rise attempts):
{asc_text}

🧲 Clumping (vertical proximity):
{fmt(clumps, "🧲")}

💥 Collisions (same height, opposing drift):
{fmt(collisions, "💥")}

🌪️ Turbulence (rapid divergence):
{fmt(turbulence, "🌪️")}

🔼 Mutual Lift (similar rise force):
{fmt(lifts, "🔼")}

=======================================================================
""".strip()

        return {
            "type": "l_level_view",
            "text": frame
        }

    # --------------------------------------------------------
    # ORCHESTRATOR-COMPATIBLE RENDER(packet)
    # --------------------------------------------------------
    def render(self, packet):
        """
        The orchestrator passes a packet, but this viewer uses
        stored L‑Level frames from receive_packet(). We ignore
        the incoming packet and render the stored Phase‑E frame.
        """
        frame = self.render_original()
        if not frame:
            return ["(no L‑Level data)"]

        text = frame.get("text", "")
        return text.split("\n")

    # --------------------------------------------------------
    # TICK — emit frame
    # --------------------------------------------------------
    def tick(self):
        frame = self.render_original()
        if not frame:
            return

        self.creature.universal_bus.emit(
            source="l_level_viewer",
            channel="visual",
            kind="l_level_view",
            payload=frame
        )
