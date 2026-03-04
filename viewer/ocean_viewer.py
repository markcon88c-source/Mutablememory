# ============================================================
# OCEAN SPACE VIEWER — CATHEDRAL OCEAN-PHYSICS + INTERACTION ENGINE
# ============================================================
# Shows:
#   - Per-packet ocean physics (drift, depth, buoyancy, currents)
#   - Multi-sentence interactions (clumping, bonding, repulsion, turbulence)
#   - Cluster attractors
#   - Fully orchestrator-compatible render(packet)
# ============================================================

class OceanViewer:
    def __init__(self, creature=None):
        self.creature = creature
        self.frames = []   # store last 10 ocean packets

    # --------------------------------------------------------
    # RECEIVE PACKET (bus mode)
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("channel") != "ocean":
            return

        payload = packet.get("payload")
        if payload:
            self.frames.append(payload)

        # Keep last 10 frames
        self.frames = self.frames[-10:]

    # --------------------------------------------------------
    # INTERACTION ANALYSIS (multi-sentence)
    # --------------------------------------------------------
    def analyze_interactions(self):
        if len(self.frames) < 2:
            return [], [], [], []

        clumps = []
        bonds = []
        repulsions = []
        turbulence = []

        for i in range(len(self.frames)):
            for j in range(i + 1, len(self.frames)):
                a = self.frames[i]
                b = self.frames[j]

                # Distance = depth + drift difference
                dist = abs(a.get("depth", 0) - b.get("depth", 0)) \
                     + abs(a.get("drift", 0) - b.get("drift", 0))

                # Clumping
                if dist < 3:
                    clumps.append((a.get("id", "?"), b.get("id", "?")))

                # Bonding (shared currents)
                ac = set(a.get("currents", {}).keys())
                bc = set(b.get("currents", {}).keys())
                if ac & bc:
                    bonds.append((a.get("id", "?"), b.get("id", "?")))

                # Repulsion (opposite drift)
                if a.get("drift", 0) * b.get("drift", 0) < 0:
                    repulsions.append((a.get("id", "?"), b.get("id", "?")))

                # Turbulence (depth shock)
                if abs(a.get("depth", 0) - b.get("depth", 0)) > 5:
                    turbulence.append((a.get("id", "?"), b.get("id", "?")))

        return clumps, bonds, repulsions, turbulence

    # --------------------------------------------------------
    # UTILITY: bar meter
    # --------------------------------------------------------
    def _bar(self, value, width=20):
        value = max(0.0, min(1.0, value))
        filled = int(value * width)
        return "[" + ("█" * filled) + ("-" * (width - filled)) + "]"

    # --------------------------------------------------------
    # ORIGINAL RENDER (kept intact)
    # --------------------------------------------------------
    def render_original(self):
        if not self.frames:
            return None

        clumps, bonds, repulsions, turbulence = self.analyze_interactions()

        def fmt(pairs, emoji):
            return "\n".join(f"  {emoji} {a} ↔ {b}" for a, b in pairs) if pairs else "  (none)"

        frame = f"""
===================== 🌊 OCEAN SPACE VIEWER 🌊 =====================

🌐 Active Sentences: {len(self.frames)}

🧲 Clumping (close proximity):
{fmt(clumps, "🧲")}

🔗 Bonding (shared currents):
{fmt(bonds, "🔗")}

🌀 Repulsion (opposite drift):
{fmt(repulsions, "🌀")}

🌪️ Turbulence (rapid change):
{fmt(turbulence, "🌪️")}

====================================================================
""".strip()

        return {
            "type": "ocean_view",
            "text": frame
        }

    # --------------------------------------------------------
    # ORCHESTRATOR-COMPATIBLE RENDER(packet)
    # --------------------------------------------------------
    def render(self, packet):
        """
        The orchestrator passes a packet, but this viewer uses
        stored frames from receive_packet(). We ignore the
        incoming packet and render the stored ocean frame.
        """
        frame = self.render_original()
        if not frame:
            return ["(no ocean data)"]

        text = frame.get("text", "")
        return text.split("\n")

    # --------------------------------------------------------
    # TICK — emit frame to the universal bus
    # --------------------------------------------------------
    def tick(self):
        frame = self.render_original()
        if not frame:
            return

        self.creature.universal_bus.emit(
            source="ocean_space_viewer",
            channel="visual",
            kind="ocean_view",
            payload=frame
        )
