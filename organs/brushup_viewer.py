# organs/brushup_viewer.py

class BrushupViewer:
    def __init__(self, creature):
        self.creature = creature

    def show(self):
        field = self.creature.english_field

        print("🧹 BRUSH‑UP VIEW")
        print("────────────────────────────────────────────")

        print("Chosen Word:")
        print(f"  {field.chosen_word}\n")

        print("Candidates:")
        for c in field.candidate_words:
            print(f"  {c}")
        print()

        print("Force Profile:")
        for k, v in field.force_profile.items():
            print(f"  {k:<10}: {v:.2f}")
        print()

        print("Sentence Context:")
        print(f"  {field.sentence_context}\n")

        print("Source Bucket:")
        print(f"  {field.source_bucket}")
