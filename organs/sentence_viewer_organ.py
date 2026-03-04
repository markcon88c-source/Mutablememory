# organs/sentence_viewer_organ.py

class SentenceViewerOrgan:
    """
    Displays the creature's most recent sentence fragment in a clean,
    scroll‑friendly panel. Works with the updated metabolic loop.
    """

    def __init__(self, creature):
        self.creature = creature

    def show(self):
        frag = getattr(self.creature, "last_sentence_fragment", None)

        print("📝 SENTENCE VIEW")
        print("────────────────────────────────────────────")

        if not frag:
            print("No sentence fragment available.")
            return

        # Words list
        words = frag.get("words", [])
        print(f"Words: {words}")

        # Full brushed sentence
        sentence = frag.get("sentence", "")
        print(f"Sentence: {sentence}")

        # Stability + green
        stability = frag.get("stability")
        green = frag.get("green")
        print(f"Stability: {stability}")
        print(f"Green: {green}")

        # Dominant force
        dom = frag.get("dominant_force")
        print(f"Dominant Force: {dom}")

        # Story type (if present)
        stype = frag.get("story_type")
        if stype:
            print(f"Story Type: {stype}")
