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
