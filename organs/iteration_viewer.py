# organs/iteration_viewer.py

class IterationViewer:
    def __init__(self, creature):
        self.creature = creature

    def show(self, meta, packets=None, iteration=1, total=1):
        if not meta:
            print("No meta available.")
            return

        print("📐 ITERATION STRUCTURE VIEW")
        print("────────────────────────────────────────────")
        print(f"Iteration {iteration}/{total}\n")

        struct = meta.get("structure_attempt", {})
        print("🔹 Structure Attempt")
        print(f"  Subject : {struct.get('subject')}")
        print(f"  Verb    : {struct.get('verb')}")
        print(f"  Object  : {struct.get('object')}")
        print(f"  Modifier: {struct.get('modifier')}\n")

        print("🔹 Stability")
        print(f"  Value         : {meta.get('stability')}")
        print(f"  Classification: unknown\n")

        forces = meta.get("force_output", {}).get("force_values", {})
        print("🔹 Forces")
        for k, v in forces.items():
            print(f"  {k.capitalize():<7}: {v:.2f}")
        print()

        print("🔹 Green")
        print(f"  Green score: {meta.get('green')}\n")

        print("🔹 Sentence")
        print(f"  {meta.get('brushed_sentence')}")
