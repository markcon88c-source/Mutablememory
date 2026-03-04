# ============================================================
# CHARACTER VIEWER ORGAN — CATHEDRAL CHARACTER FRAME EYE
# Turns character sheets, identity packets, and birth packets
# into a unified visualizable character-frame.
# Now updated to pull mutated identity packets from NameHeart.
# ============================================================

class CharacterViewerOrgan:
    """
    The CharacterViewerOrgan is the creature's ability to
    visually 'see' characters: their name, forces, stats,
    alignment, and origin. It produces a character-frame
    packet that StoryViewer and ViewerOrgan can use.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_character = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        ptype = packet.get("kind")

        # Accept character sheets
        if ptype == "character_sheet":
            self.last_character = packet.get("payload")

        # Accept birth packets
        if ptype == "birth":
            self.last_character = packet.get("payload")

        # Accept identity-only packets
        if ptype == "character_idea":
            self.last_character = {
                "name": packet.get("mutated"),
                "origin_name": packet.get("base"),
                "role": packet.get("role"),
                "seed": packet.get("seed"),
                "forces": {},
                "stats": {},
                "alignment": "Unknown"
            }

        # --------------------------------------------------------
        # NEW: Accept mutated identity packets from NameHeart
        # --------------------------------------------------------
        if packet.get("channel") == "character" and packet.get("kind") == "mutated_identity":
            payload = packet.get("payload", {})

            if not self.last_character:
                self.last_character = {}

            # Update identity fields
            self.last_character["name"] = payload.get("name")
            self.last_character["surname"] = payload.get("surname")
            self.last_character["full_name"] = payload.get("full_name")
            self.last_character["letters"] = payload.get("letters")
            self.last_character["cluster"] = payload.get("cluster")
            self.last_character["force_type"] = payload.get("force_type")
            self.last_character["force_target"] = payload.get("force_target")
            self.last_character["mode"] = payload.get("mode")
            self.last_character["seed"] = payload.get("seed")
            self.last_character["block_id"] = payload.get("block_id")

    # --------------------------------------------------------
    # TICK — emit character-frame
    # --------------------------------------------------------
    def tick(self):
        if not self.last_character:
            return

        frame = {
            "type": "character_frame",
            "character": self.last_character
        }

        self.creature.universal_bus.emit(
            source="character_viewer",
            channel="visual",
            kind="character_frame",
            payload=frame
        )


# ============================================================
# CHARACTER VIEWER — EMOJI EXPRESSIVE CATHEDRAL VIEWER
# Orchestrator‑compatible edition (keeps all your style)
# ============================================================

class CharacterViewer:
    """
    The CharacterViewer is the expressive perception layer.
    It takes character-frame packets and renders them into
    a mythic, emoji-rich character card — now orchestrator-safe.
    """

    FORCE_EMOJIS = {
        "pulse": "💓",
        "tone": "🎼",
        "spark": "⚡",
        "drift": "🍃",
        "echo": "🔊",
        "chaos": "🌀",
        "clarity": "✨",
        "memory": "📚",
        "pressure": "🌡️",
    }

    STAT_EMOJIS = {
        "strength": "💪",
        "will": "🧠",
        "insight": "🔮",
        "presence": "🌟",
        "luck": "🍀",
    }

    ALIGNMENT_EMOJIS = {
        "Lawful": "⚖️",
        "Neutral": "🔸",
        "Chaotic": "🔥",
        "Good": "🌈",
        "Evil": "🌑",
    }

    def __init__(self, creature):
        self.creature = creature
        self.last_frame = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("kind") != "character_frame":
            return
        self.last_frame = packet.get("payload", {})

    # --------------------------------------------------------
    # INTERNAL RENDER — returns a single string
    # --------------------------------------------------------
    def _render_internal(self):
        if not self.last_frame:
            return "=== 🧿 CHARACTER VIEWER 🧿 ===\n(no character frames yet)"

        char = self.last_frame.get("character", {})

        name = char.get("name", "Unknown")
        role = char.get("role", "Unknown")
        alignment = char.get("alignment", "Neutral Neutral")
        origin = char.get("origin_name", "")
        forces = char.get("forces", {})
        stats = char.get("stats", {})

        # Alignment emojis
        try:
            moral, ethic = alignment.split()
        except:
            moral, ethic = "Neutral", "Neutral"

        align_emoji = (
            self.ALIGNMENT_EMOJIS.get(moral, "🔸")
            + self.ALIGNMENT_EMOJIS.get(ethic, "🔸")
        )

        # Build force lines
        force_lines = []
        for key, val in forces.items():
            emoji = self.FORCE_EMOJIS.get(key, "❔")
            bar = emoji * max(1, int(val))
            force_lines.append(f"{emoji} {key.capitalize():<8} {bar}")

        # Build stat lines
        stat_lines = []
        for key, val in stats.items():
            emoji = self.STAT_EMOJIS.get(key, "❔")
            stat_lines.append(f"{emoji} {key.capitalize():<8} {val}")

        text = f"""
================= 🧿 CHARACTER VIEWER 🧿 =================

👤 Name: {name}
🎭 Role: {role}
🪞 Origin: {origin}
🧭 Alignment: {align_emoji}  {alignment}

----------------- ⚡ Forces ⚡ -----------------
{chr(10).join(force_lines)}

----------------- 📊 Stats 📊 -----------------
{chr(10).join(stat_lines)}

===========================================================
""".strip()

        return text

    # --------------------------------------------------------
    # ORCHESTRATOR RENDER — returns list[str]
    # --------------------------------------------------------
    def render(self, packet):
        text = self._render_internal()
        return text.split("\n")

    # --------------------------------------------------------
    # TICK — emit rendered card
    # --------------------------------------------------------
    def tick(self):
        text = self._render_internal()
        if not text:
            return

        self.creature.universal_bus.emit(
            source="character_viewer",
            channel="visual",
            kind="character_view",
            payload={
                "type": "character_view",
                "text": text
            }
        )
