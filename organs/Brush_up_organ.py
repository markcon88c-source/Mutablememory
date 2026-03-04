# ============================================================
# BRUSH-UP ORGAN — Cathedral Edition (Aligned Version)
# ============================================================

class BrushUpOrgan:
    """
    Produces a refinement packet for the BrushUpViewer.
    Reads from english_field and emits:
      - sentence
      - candidates
      - scores
      - emerald_level
      - stability
      - ascension_state
      - summary
      - cycle
    """

    def __init__(self, creature):
        self.creature = creature
        self.cycle = 0
        self.last_packet = None

    def tick(self, creature):
        self.cycle += 1

        # Pull sentence from EnglishFieldOrgan
        field = creature.english_field
        sentence = getattr(field, "phrase", "")

        # Simple candidate generation
        words = sentence.split()
        candidates = [sentence, sentence.upper(), sentence.lower()]
        scores = [len(sentence), len(words), len(sentence) % 7]

        packet = {
            "cycle": self.cycle,
            "sentence": sentence,
            "candidates": candidates,
            "scores": scores,
            "emerald_level": min(100, len(sentence) * 2),
            "stability": len(words),
            "ascension_state": "stable" if len(words) > 0 else "void",
            "summary": f"{len(words)} words processed."
        }

        self.last_packet = packet
        return packet
