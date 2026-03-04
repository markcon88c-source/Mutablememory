# organs/sentence_pool_viewer.py
# Expressive Sentence Pool Viewer with cinematic movie‑credit scroll

import time


class SentencePoolViewer:
    def __init__(self):
        # Movie‑credit scroll speed (seconds per sentence block)
        self.scroll_delay = 0.55   # ← tuned for cinematic pacing

    # ------------------------------------------------------------
    # Utility Bars
    # ------------------------------------------------------------
    def _bar(self, value, max_len=20, emoji="🟦"):
        try:
            v = int(value)
        except:
            v = 0
        v = max(0, min(v, max_len))
        return emoji * v + "▫️" * (max_len - v)

    # ------------------------------------------------------------
    # Story Type Emoji Mapping
    # ------------------------------------------------------------
    def _story_emoji(self, story_type):
        mapping = {
            "drama": "🎭",
            "tragedy": "💔",
            "comedy": "😂",
            "romance": "💗",
            "horror": "👻",
            "mystery": "🕵️",
            "adventure": "🗺️",
            "epic": "🏔️",
            "mythic": "🐉",
            "dream": "💤",
            "surreal": "🌀",
            "sci_fi": "🚀",
            "fantasy": "🧙",
            "chaos": "🌪️",
            "slice_of_life": "☕",
            "philosophical": "📚",
            "spiritual": "🕊️",
            "heroic": "🛡️",
            "melancholic": "🌧️",
            "cosmic": "🌌",
        }
        return mapping.get(story_type, "✨")

    # ------------------------------------------------------------
    # Cluster Hint
    # ------------------------------------------------------------
    def _cluster_hint(self, sentence):
        s = sentence.lower()
        if "chaos" in s:
            return "🌪 chaos‑leaning"
        if "love" in s:
            return "💗 heart‑cluster"
        if "dark" in s:
            return "🌑 shadow‑cluster"
        if "light" in s:
            return "🌞 radiance‑cluster"
        return "✨ neutral drift"

    # ------------------------------------------------------------
    # Mood Emoji
    # ------------------------------------------------------------
    def _mood_emoji(self, score):
        if score > 0.8:
            return "😇"
        if score > 0.6:
            return "🙂"
        if score > 0.4:
            return "😐"
        if score > 0.2:
            return "😕"
        return "😖"

    # ------------------------------------------------------------
    # MAIN DISPLAY (PACKET-DRIVEN)
    # ------------------------------------------------------------
    def display(self, packets):
        """
        packets: list of packet dicts
        We look for a packet with:
            packet["type"] == "sentence_pool"
            packet["pool"] == list of sentence dicts
        """

        # Extract pool
        pool = None
        for p in packets:
            if p.get("type") == "sentence_pool":
                pool = p.get("pool", [])
                break

        print("\n\n🌀🌀🌀  SENTENCE POOL VIEWER  🌀🌀🌀")
        print("=====================================\n")

        if not pool:
            print("⚠️ No sentence_pool packet found.\n")
            return

        # --------------------------------------------------------
        # CINEMATIC MOVIE‑CREDIT SCROLL
        # --------------------------------------------------------
        for idx, s in enumerate(pool, 1):
            time.sleep(self.scroll_delay)  # ← slow, cinematic

            text = s.get("text", "")
            glue = s.get("glue", 0.0)
            math_block = s.get("math_block", 0.0)
            force = s.get("force", 0.0)
            rarity = s.get("rarity", 0.0)
            mood = s.get("mood", 0.0)
            story_type = s.get("story_type", "unknown")

            story_icon = self._story_emoji(story_type)

            print(f"🔹 Sentence {idx}")
            print(f"💬 {text}")
            print(f"🏷️ story type: {story_icon}  {story_type}")
            print(f"🔍 cluster: {self._cluster_hint(text)}")
            print(f"🎭 mood: {self._mood_emoji(mood)}  ({mood:.2f})")

            print("\n📊 Metrics:")
            print(f"   🧲 glue:       {glue:.2f}   {self._bar(glue*20, emoji='🟩')}")
            print(f"   🔢 math:       {math_block:.2f}   {self._bar(math_block*20, emoji='🟪')}")
            print(f"   ⚡ force:      {force:.2f}   {self._bar(force*20, emoji='🟥')}")
            print(f"   🌟 rarity:     {rarity:.2f}   {self._bar(rarity*20, emoji='🟨')}")

            if rarity > 0.85:
                print("   🎰 JACKPOT RARITY HIT! 🎰")
            if force > 0.9:
                print("   💥 FORCE SPIKE DETECTED 💥")
            if glue < 0.1:
                print("   🧊 LOW‑GLUE FRAGMENT 🧊")

            print("\n-------------------------------------\n")
