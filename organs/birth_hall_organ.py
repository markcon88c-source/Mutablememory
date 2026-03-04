# ============================================================
# BIRTH HALL ORGAN — CATHEDRAL DESCENT CHAMBER
# Receives character-frame packets and renders the Birth Hall.
# ============================================================

class BirthHallOrgan:
    """
    The BirthHallOrgan listens for character-frame packets
    (produced by CharacterViewerOrgan) and renders a mythic
    Birth Hall scene for the current identity.
    """

    def __init__(self, creature):
        self.creature = creature
        self.current_character = None
        self.last_render = None
        self.cycle = 0

    # --------------------------------------------------------
    # RECEIVE PACKET — pull from CharacterViewerOrgan
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("kind") != "character_frame":
            return

        frame = packet.get("payload", {})
        self.current_character = frame.get("character", {})

    # --------------------------------------------------------
    # INTERNAL RENDER — build the Birth Hall scene
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.current_character:
            return "=== 🕳️ BIRTH HALL ===\n(no identity has descended yet)"

        char = self.current_character

        name = char.get("name", "Unknown")
        origin = char.get("origin_name", "Unknown")
        role = char.get("role", "Unknown")
        alignment = char.get("alignment", "Neutral Neutral")
        forces = char.get("forces", {})
        stats = char.get("stats", {})

        # Build force lines
        force_lines = []
        for key, val in forces.items():
            bar = "█" * max(1, int(val))
            force_lines.append(f"{key.capitalize():<10} {bar}")

        # Build stat lines
        stat_lines = []
        for key, val in stats.items():
            stat_lines.append(f"{key.capitalize():<10} {val}")

        text = f"""
===================== 🕳️ BIRTH HALL 🕳️ =====================

A hush falls across the Cathedral.

From the deep chambers of the Naming Heart,
a new identity descends into the Birth Hall…

✨ Name: {name}
🪞 Origin: {origin}
🎭 Role: {role}
🧭 Alignment: {alignment}

--------------------- Forces ---------------------
{chr(10).join(force_lines)}

---------------------- Stats ----------------------
{chr(10).join(stat_lines)}

The Cathedral acknowledges their arrival.
===================================================
""".strip()

        return text

    # --------------------------------------------------------
    # TICK — emit Birth Hall scene
    # --------------------------------------------------------
    def tick(self):
        self.cycle += 1
        text = self._render_internal()
        self.last_render = text

        self.creature.universal_bus.emit(
            source="birth_hall",
            channel="visual",
            kind="birth_hall_view",
            payload={
                "type": "birth_hall_view",
                "text": text
            }
        )
