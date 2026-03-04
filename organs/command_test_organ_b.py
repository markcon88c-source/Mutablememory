# command_test_organ_b.py
# ============================================================
# COMMAND TEST ORGAN B
# Uses a different interpretation function.
# ============================================================

class CommandTestOrganB:
    def __init__(self, creature):
        self.creature = creature

    def interpret_B(self, raw):
        return f"B classifies '{raw}' as a secondary behavior"
