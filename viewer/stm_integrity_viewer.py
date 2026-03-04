# ============================================================
# STMIntegrityViewer — Experimental Wall Viewer
# ============================================================

class STMIntegrityViewer:
    """
    Viewer for STM integrity state.
    Designed for the Experimental Wall.

    Expects:
      - packet["organs"]["stm"] snapshot
      - packet["organs"]["integrity"] snapshot (if present)
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
        lines.append(f"[STMIntegrityViewer] Tick {tick}")

        # ----------------------------------------------------
        # STM organ state
        # ----------------------------------------------------
        stm = packet["organs"].get("stm", {})
        if stm:
            memory = stm.get("memory", "?")
            focus = stm.get("focus", "?")
            load = stm.get("load", "?")
            lines.append(f"  STM: memory={memory}, focus={focus}, load={load}")

        # ----------------------------------------------------
        # Integrity organ state
        # ----------------------------------------------------
        integ = packet["organs"].get("integrity", {})
        if integ:
            score = integ.get("score", "?")
            drift = integ.get("drift", "?")
            stability = integ.get("stability", "?")
            lines.append(f"  Integrity: score={score}, drift={drift}, stability={stability}")

        # ----------------------------------------------------
        # Universal bus summary
        # ----------------------------------------------------
        bus = packet.get("bus", {})
        if bus:
            count = len(bus.get("packets", []))
            lines.append(f"  Bus packets: {count}")

        return lines
