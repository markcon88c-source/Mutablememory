# ============================================================
# VIEWER SPEC ORGAN — CATHEDRAL EDITION
#
# Purpose:
#   Attach all viewers provided by the ViewerRegistry to the
#   creature instance. Supports ANY number of viewers.
# ============================================================

class ViewerSpecOrgan:
    def __init__(self, creature):
        self.creature = creature

    def attach(self, viewers):
        """
        Attach all viewer instances to the creature dynamically.
        """
        for name, viewer in viewers.items():
            setattr(self.creature, name, viewer)
