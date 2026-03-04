# ============================================================
# CharacterBirthViewer — Party Atmosphere Edition
# ============================================================

class CharacterBirthViewer:
    """
    Celebratory viewer for character birth events.
    Party-themed but fully Cathedral-physiology compliant.

    Expects:
      - packet["organs"]["character_birth"] snapshot
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
        lines.append(f"[CharacterBirthViewer] 🎊 Tick {tick}")

        # ----------------------------------------------------
        # Character birth organ state
        # ----------------------------------------------------
        birth = packet["organs"].get("character_birth", {})
        if birth:
            name = birth.get("name", "?")
            archetype = birth.get("archetype", "?")
            spark = birth.get("spark", "?")

            # Party glyphs
            name_glyph = "🎉" if name != "?" else "✨"
            arch_glyph = "🎭" if archetype != "?" else "❔"
            spark_glyph = "⚡" if spark != "?" else "·"

            lines.append(f"  {name_glyph} New Character: {name}")
            lines.append(f"  {arch_glyph} Archetype: {archetype}")
            lines.append(f"  {spark_glyph} Spark: {spark}")

            # Party atmosphere line
            lines.append("  🎈🎈 A new presence enters the Cathedral! 🎈🎈")

        # ----------------------------------------------------
        # Universal bus summary
        # ----------------------------------------------------
        bus = packet.get("bus", {})
        if bus:
            count = len(bus.get("packets", []))
            glyph = "🪩" if count > 0 else "🔇"
            lines.append(f"  Bus {glyph}: {count} packets dancing through the system")

        return lines
