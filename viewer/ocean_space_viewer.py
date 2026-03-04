# ============================================================
# OceanSpaceViewer — Experimental Wall Viewer
# ============================================================

class OceanSpaceViewer:
    """
    Viewer that blends ocean-depth metaphors with space-scale
    narrative physics. Designed for the Experimental Wall.

    Expects:
      - packet["bus"] from UniversalBusOrgan.snapshot()
      - packet["organs"][...] snapshots
      - narrative physics fields if present
    """

    def __init__(self, creature):
        self.creature = creature

    def render(self, packets):
        if not packets:
            return []

        packet = packets[-1]
        lines = []

        tick = packet.get("tick", 0)
        lines.append(f"[OceanSpaceViewer] Tick {tick}")

        # ----------------------------------------------------
        # Ocean layer (depth, drift, undercurrents)
        # ----------------------------------------------------
        ocean = packet["organs"].get("ocean", {})
        if ocean:
            depth = ocean.get("depth", "?")
            drift = ocean.get("drift", "?")
            lines.append(f"  Ocean: depth={depth}, drift={drift}")

        # ----------------------------------------------------
        # Space layer (vectors, attractors, gravity wells)
        # ----------------------------------------------------
        space = packet["organs"].get("space", {})
        if space:
            vectors = space.get("vectors", "?")
            wells = space.get("gravity_wells", "?")
            lines.append(f"  Space: vectors={vectors}, wells={wells}")

        # ----------------------------------------------------
        # Narrative physics (story type, forces, attractors)
        # ----------------------------------------------------
        story = packet["organs"].get("story_type", {})
        if story:
            stype = story.get("type", "?")
            attractor = story.get("attractor", "?")
            lines.append(f"  StoryType: {stype}, attractor={attractor}")

        # ----------------------------------------------------
        # Universal bus summary
        # ----------------------------------------------------
        bus = packet.get("bus", {})
        if bus:
            count = len(bus.get("packets", []))
            lines.append(f"  Bus packets: {count}")

        return lines
