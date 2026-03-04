# ============================================================
# IDEA ENGINE ORGAN — Cathedral Edition (Aligned Version)
# ============================================================

import random

class IdeaEngineOrgan:
    """
    Emits evolving idea-state packets each heartbeat.
    Cathedral-compatible: accepts creature, uses tick(creature),
    and stores last_packet for viewers.
    """

    def __init__(self, creature):
        self.creature = creature
        self.cycle = 0
        self.last_packet = None

        self.idea_pool = [
            "a forming concept",
            "a drifting intention",
            "a soft hypothesis",
            "a rising intuition",
            "a symbolic spark",
            "a quiet inference",
            "a structural hint",
            "a narrative seed",
            "a subtle connection",
            "a warm insight"
        ]

    def _generate_idea(self):
        return random.choice(self.idea_pool)

    def tick(self, creature):
        self.cycle += 1
        idea = self._generate_idea()

        packet = {
            "cycle": self.cycle,
            "idea": idea,
            "state": "forming" if idea else "empty"
        }

        self.last_packet = packet
        return packet
