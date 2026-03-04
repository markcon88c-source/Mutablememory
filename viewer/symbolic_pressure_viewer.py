# ============================================================
# SymbolicPressureViewer — Symbolic / Mythic Edition
# ============================================================

class SymbolicPressureViewer:
    """
    Symbolic viewer for pressure fields.
    Uses glyphs and mythic metaphors while staying
    fully compatible with Cathedral physiology.

    Expects:
      - packet["organs"]["symbolic_pressure"]
      - packet["bus"]
    """

    def __init__(self, creature):
        self.creature = creature

    def render(self, packets):
        if not packets:
            return []

        packet = packets[-1]
        lines = []

        tick = packet.get("tick", 0)
        lines.append(f"[SymbolicPressureViewer] ⌁ Tick {tick}")

        # ----------------------------------------------------
        # Symbolic pressure organ state
        # ----------------------------------------------------
        sp = packet["organs"].get("symbolic_pressure", {})
        if sp:
            pressure = sp.get("pressure", "?")
            gradient = sp.get("gradient", "?")
            flux = sp.get("flux", "?")

            # Symbolic glyphs
            p_glyph = "⟡" if pressure != "?" else "·"
            g_glyph = "⇀" if gradient != "?" else "·"
            f_glyph = "↯" if flux != "?" else "·"

            lines.append(f"  Pressure {p_glyph}: {pressure}")
            lines.append(f"  Gradient {g_glyph}: {gradient}")
            lines.append(f"  Flux {f_glyph}: {flux}")

        # ----------------------------------------------------
        # Universal bus summary
        # ----------------------------------------------------
        bus = packet.get("bus", {})
        if bus:
            count = len(bus.get("packets", []))
            glyph = "☉" if count > 0 else "○"
            lines.append(f"  Bus {glyph}: {count} packets in circulation")

        return lines
