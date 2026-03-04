# ============================================================
# STORY VIEWER — EMOJI EXPRESSIVE CATHEDRAL NARRATIVE VIEWER
# Combines character_view + world_idea + forces into a story frame.
# ============================================================

class StoryViewer:
    """
    The StoryViewer is the expressive narrative perception layer.
    It listens for character_view packets, world_idea packets,
    and birth/identity packets, and renders a mythic story-frame.
    """

    WORLD_EMOJIS = {
        "conflict": "⚔️",
        "journey": "🛤️",
        "mystery": "🕯️",
        "growth": "🌱",
        "cosmic": "🌌",
        "dream": "💭",
        "shadow": "🌑",
        "light": "✨",
    }

    def __init__(self, creature):
        self.creature = creature
        self.last_character = None
        self.last_world = None
        self.last_birth = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        kind = packet.get("kind")
        ptype = packet.get("type")

        # Character view
        if kind == "character_view":
            self.last_character = packet.get("payload")

        # World idea
        if ptype == "world_idea":
            self.last_world = packet.get("idea")

        # Birth packet
        if kind == "birth":
            self.last_birth = packet.get("payload")

    # --------------------------------------------------------
    # RENDER STORY FRAME
    # --------------------------------------------------------
    def render(self):
        if not self.last_character:
            return None

        char = self.last_character
        name = char.get("name", "Unknown")
        role = char.get("role", "Unknown")
        alignment = char.get("alignment", "Neutral")
        forces = char.get("forces", {})
        stats = char.get("stats", {})

        # World idea emoji
        world_text = self.last_world or "Unknown"
        world_emoji = "🌍"
        for key, emoji in self.WORLD_EMOJIS.items():
            if key in world_text.lower():
                world_emoji = emoji
                break

        # Birth info
        birth_line = ""
        if self.last_birth:
            seed = self.last_birth.get("seed", "")
            birth_line = f"🍼 Born from seed: {seed}"

        # Build story frame text
        frame_text = f"""
===================== 📖 STORY VIEWER 📖 =====================

👤 Character: {name}
🎭 Role: {role}
🧭 Alignment: {alignment}

{birth_line}

--------------------- 🌍 World Context ----------------------
{world_emoji} {world_text}

--------------------- 🔮 Narrative Pulse ---------------------
This being moves through the world with:

- Forces: {', '.join(f"{k}:{v}" for k,v in forces.items())}
- Stats: {', '.join(f"{k}:{v}" for k,v in stats.items())}

A story is forming around them…

==============================================================
""".strip()

        return {
            "type": "story_view",
            "text": frame_text
        }

    # --------------------------------------------------------
    # TICK — emit story frame
    # --------------------------------------------------------
    def tick(self):
        frame = self.render()
        if not frame:
            return

        self.creature.universal_bus.emit(
            source="story_viewer",
            channel="visual",
            kind="story_view",
            payload=frame
        )
