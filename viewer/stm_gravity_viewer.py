# ============================================================
# STMGravityViewer — Experimental Wall Viewer
# ============================================================

class STMGravityViewer:
    """
    Viewer for STM + narrative gravity interactions.
    Designed for the Experimental Wall.

    Expects:
      - packet["organs"]["stm"] snapshot
      - packet["organs"]["story_gravity"] snapshot (if present)
      - packet["bus"] from UniversalBusOrgan.snapshot()
    """

    def __init__(self, creature):
        self.creature = creature

    def render(self, packets):
        if not packets:
            return []

        packet = packets[-1]
        lines = []

        tick = packet.get("tick", 0)
        lines.append(f"[STMGravityViewer] Tick {tick}")

        # ----------------------------------------------------
        # STM organ state
        # ----------------------------------------------------
        stm = packet["organs"].get("stm", {})
        if stm:
            memory = stm.get("memory", "?")
            focus = stm.get("focus", "?")
            lines.append(f"  STM: memory={memory}, focus={focus}")

        # ----------------------------------------------------
        # Narrative gravity (story forces)
        # ----------------------------------------------------
        gravity = packet["organs"].get("story_gravity", {})
        if gravity:
            vectors = gravity.get("vectors", "?")
            wells = gravity.get("wells", "?")
            lines.append(f"  Gravity: vectors={vectors}, wells={wells}")

        # ----------------------------------------------------
        # Universal bus summary
        # ----------------------------------------------------
        bus = packet.get("bus", {})
        if bus:
            count = len(bus.get("packets", []))
            lines.append(f"  Bus packets: {count}")

        return lines
