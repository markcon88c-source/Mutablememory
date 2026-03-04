import random

class WorldbuildingOrgan:
    """
    Generates a simple English world-line based on thought + pressures.
    Safe, non-breaking, minimal.
    """

    def __init__(self):
        self.templates = [
            "the {symbolic_adj} {noun} drifts beneath {phrase}",
            "a {symbolic_adj} current gathers around {phrase}",
            "the air thickens with {symbolic_adj} meaning near {phrase}",
            "a quiet shift moves through the {noun} as {phrase} forms",
            "{phrase} settles into the {symbolic_adj} field"
        ]

        self.nouns = ["horizon", "field", "air", "path", "stillness"]

        self.symbolic_words = [
            "soft", "bright", "heavy", "thin", "rising", "flickering"
        ]

    def generate(self, thought_packet):
        if not isinstance(thought_packet, dict):
            return None

        phrase = thought_packet.get("phrase", "soft air")
        symbolic = thought_packet.get("symbolic", 0.5)

        # Map symbolic pressure to an adjective
        idx = int(symbolic * (len(self.symbolic_words) - 1))
        idx = max(0, min(len(self.symbolic_words) - 1, idx))
        symbolic_adj = self.symbolic_words[idx]

        noun = random.choice(self.nouns)
        template = random.choice(self.templates)

        line = template.format(
            symbolic_adj=symbolic_adj,
            noun=noun,
            phrase=phrase
        )

        return {
            "english": line,
            "symbolic_adj": symbolic_adj,
            "noun": noun,
            "phrase": phrase
        }
