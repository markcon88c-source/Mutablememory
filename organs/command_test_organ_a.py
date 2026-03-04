# command_test_organ_a.py
# ============================================================
# COMMAND TEST ORGAN A
# Uses one interpretation function.
# ============================================================

class CommandTestOrganA:
    def __init__(self, creature):
        self.creature = creature

    def interpret_A(self, raw):
        return f"A sees '{raw}' as a primary action"
