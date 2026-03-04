# organs/language_viewer_organ.py

class LanguageViewerOrgan:
    """
    Cathedral-era Language Viewer Organ.
    Provides a full cathedral-shaped result so viewer/language_viewer.py
    never crashes, even when the metabolic system is the real engine.
    """

    def __init__(self, creature):
        self.creature = creature

    # ---------------------------------------------------------
    # CATHEDRAL v5 COMPATIBILITY LAYER
    # ---------------------------------------------------------
    def process_sentence(self, words):
        """
        Returns a cathedral-shaped result dict.
        Prevents KeyErrors in the viewer and preserves metabolic meta.
        """

        meta = getattr(self.creature, "last_meta", {}) or {}
        packets = getattr(self.creature, "last_packets", []) or []

        stability = meta.get("stability", 0.0)

        # Minimal fake iteration structure (4 breaths)
        iterations = []
        for i in range(1, 5):
            iterations.append({
                "iteration": i,
                "words": words,
                "stability": stability,
                "notes": "metabolic‑compat stub"
            })

        return {
            "raw_words": words,
            "initial_stability": stability,
            "iterations": iterations,
            "rejected": [],
            "final_words": words,
            "final_stability": stability,
            "story_type": meta.get("story_type", "unknown"),
            "story_destiny": meta.get("story_destiny", "unknown"),
            "brushups": [],
            "structure_alignment": "neutral",

            # Preserve metabolic data
            "packets": packets,
            "meta": meta,
        }

    # ---------------------------------------------------------
    # MODERN METABOLIC VIEWER (unchanged)
    # ---------------------------------------------------------
    def show(self, meta, packets=None):
        print("🗣️ LANGUAGE VIEW (after metabolic handoff)")
        print("────────────────────────────────────────────")

        if not meta:
            print("No language meta available.")
            return

        stability = meta.get("stability")
        print(f"Metabolic Stability: {stability}")

        print("Zone: None")

        attempts = getattr(self.creature.emergence, "attempts", None)
        if attempts is not None:
            print(f"Attempts since last GREEN: {attempts}")
        else:
            print("Attempts since last GREEN: (no emergence organ)")

        if packets:
            print("\nPackets:")
            for p in packets:
                print(f"  {p}")
