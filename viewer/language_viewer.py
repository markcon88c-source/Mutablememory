# ============================================================
# LANGUAGE VIEWER — EMERALD ASCENSION EDITION (identity-aware)
# Displays emerald physiology + refusal + character identity.
# ============================================================

class LanguageViewer:
    """
    The Emerald Ascension Language Viewer.
    Displays the full emerald physiology emitted by the
    Emerald Ascension LanguageOrgan, including refusal_state
    and the current character identity.
    """

    def __init__(self, creature=None):
        self.creature = creature
        self.last_packet = None

    # --------------------------------------------------------
    # RECEIVE PACKET
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("channel") == "language":
            self.last_packet = packet.get("payload")

    # --------------------------------------------------------
    # INTERNAL RENDER (identity-aware)
    # --------------------------------------------------------
    def _render_internal(self):
        p = self.last_packet
        if not p:
            return None

        # NEW: identity pulled from LanguageOrgan
        character_name = p.get("character_name", "")

        words = " ".join(p.get("words", []))
        sentence = p.get("sentence", "")
        expression = p.get("expression", "")
        stability = p.get("stability", 0)
        emerald = p.get("emerald_level", 0)
        asc = p.get("ascension_state", "")
        ready = p.get("ready_for_transition", False)
        refusal = p.get("refusal_state", "none")

        refusal_emoji = {
            "none": "🟢",
            "soft": "🟡",
            "hold": "🟠",
            "deny": "🔴",
        }.get(refusal, "⚪")

        frame = f"""
================= 💚 EMERALD ASCENSION — LANGUAGE VIEWER 💚 =================

👤 Character:
  {character_name}

📝 Words:
  {words}

🗣️ Sentence:
  {sentence}

🎨 Expression:
  {expression}

✨ Stability:        {stability}
🟩 Emerald Level:   {emerald}%
🌿 Ascension:       {asc}

🚫 Refusal:         {refusal_emoji}  {refusal}

{ "💎 READY FOR TRANSITION 💚" if ready else "" }

===========================================================================
""".strip()

        return frame

    # --------------------------------------------------------
    # ORCHESTRATOR RENDER
    # --------------------------------------------------------
    def render(self, packet):
        text = self._render_internal()
        if not text:
            return ["[LanguageViewer] No language packet yet."]
        return text.split("\n")

    # --------------------------------------------------------
    # TICK — emit frame to the universal bus
    # --------------------------------------------------------
    def tick(self):
        text = self._render_internal()
        if not text:
            return

        self.creature.universal_bus.emit(
            source="language_viewer",
            channel="visual",
            kind="language_view",
            payload={
                "type": "language_view",
                "text": text
            }
        )
