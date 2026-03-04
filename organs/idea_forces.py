# organs/idea_forces.py

from decimal import Decimal


class IdeaForces:
    """
    Computes forces acting on an idea:
      • strength
      • drift
      • resonance
      • opposition
      • clustering
    """

    @staticmethod
    def compute_all(idea, all_ideas):
        s, d, r = idea.signature

        strength = Decimal(str(abs(s)))
        drift = Decimal(str(abs(d)))
        resonance = Decimal(str(abs(r)))

        # Opposition: how much this idea differs from the average signature
        if all_ideas:
            avg_s = sum(i.signature[0] for i in all_ideas) / len(all_ideas)
            avg_d = sum(i.signature[1] for i in all_ideas) / len(all_ideas)
            avg_r = sum(i.signature[2] for i in all_ideas) / len(all_ideas)
            opposition_val = abs(s - avg_s) + abs(d - avg_d) + abs(r - avg_r)
        else:
            opposition_val = 0.0

        opposition = Decimal(str(opposition_val))

        # Clustering: inverse of opposition
        clustering = Decimal("0.0")
        if opposition_val != 0:
            clustering = Decimal("1.0") / Decimal(str(1.0 + opposition_val))

        return {
            "strength": strength,
            "drift": drift,
            "resonance": resonance,
            "opposition": opposition,
            "clustering": clustering,
        }
