# organs/diagnostic_organ.py

class DiagnosticOrgan:
    """
    Emits a breadcrumb trail showing where packets stop.
    """

    def __init__(self, creature):
        self.creature = creature

    def report(self, stage, packets):
        count = 0
        if isinstance(packets, list):
            count = len(packets)

        print(f"[DIAGNOSTIC] {stage}: {count} packets")

        # Word packet count
        if isinstance(packets, list):
            words = [p for p in packets if isinstance(p, dict) and "word" in p]
            if words:
                print(f"    → {len(words)} word packets")
            else:
                print("    → NO WORD PACKETS")

        # Sentence packet count
        if isinstance(packets, list):
            sentences = [p for p in packets if isinstance(p, dict) and p.get("type") == "sentence"]
            if sentences:
                print(f"    → {len(sentences)} sentence packets")
            else:
                print("    → NO SENTENCE PACKETS")
