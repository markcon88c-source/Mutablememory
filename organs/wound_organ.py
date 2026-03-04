# organs/wound_organ.py
# ============================================================
# WOUND ORGAN — governs resurfacing, return pressure, quests
# ============================================================

import math

class WoundOrgan:
    """
    The Wound Organ governs:
      • wound pressure (desire to return)
      • resurfacing thresholds
      • chaos mobility (swimming)
      • EIX-based emergence pressure
      • depth penalty
      • symbolic suppression
      • quest generation triggers

    It does NOT store packets itself.
    It evaluates packets passed in from the Ocean Organ.
    """

    def __init__(self, creature):
        self.creature = creature

        # Tunable constants
        self.mobility_coeff = 0.45     # how well chaos becomes upward motion
        self.depth_penalty = 0.35      # how strongly depth suppresses return
        self.symbolic_supp_coeff = 0.5 # how much symbolic order pushes wounds down
        self.base_threshold = 0.6      # default return threshold

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def compute_return_potential(self, drop, tides, currents, eix):
        """
        Compute the resurfacing pressure (RP) for a wound packet.
        """

        packet = drop.get("packet", {})
        meta = packet.get("meta", {})

        # -------------------------
        # 1. Energy (dissolution)
        # -------------------------
        E = drop.get("energy", 0.5)
        wound_pressure = (1.0 - E)

        # -------------------------
        # 2. Wound factor (unresolvedness)
        # -------------------------
        weird = meta.get("weirdness", 0.0)
        drift = meta.get("drift_metrics", {}).get("value", 0.0)
        fracture = meta.get("fracture", 0.0)
        W = weird + abs(drift) + fracture

        # -------------------------
        # 3. Chaos mobility
        # -------------------------
        chaos = packet.get("chaos", 0.0)
        swim = chaos * self.mobility_coeff

        # -------------------------
        # 4. EIX emergence pressure
        # -------------------------
        phi = eix.get("Phi", 0.0)
        omega = eix.get("Omega", 0.0)
        emergence_pressure = phi + omega

        # -------------------------
        # 5. Depth penalty
        # -------------------------
        depth = drop.get("depth", 3)  # abyss = 3
        D = depth * self.depth_penalty

        # -------------------------
        # 6. Symbolic suppression
        # -------------------------
        symbolic_current = tides.get("symbolic_current", 0.0)
        S = symbolic_current * self.symbolic_supp_coeff

        # -------------------------
        # FINAL RETURN POTENTIAL
        # -------------------------
        RP = wound_pressure * W + swim + emergence_pressure - D - S
        return RP

    def compute_threshold(self, tides):
        """
        Compute the dynamic return threshold T.
        """
        drift = tides.get("drift_current", 0.0)
        chaos = tides.get("chaos_current", 0.0)
        symbolic = tides.get("symbolic_current", 0.0)

        T = (
            self.base_threshold
            - 0.4 * drift
            - 0.3 * chaos
            + 0.5 * symbolic
        )

        return max(0.1, min(T, 1.2))

    def should_resurface(self, drop, tides, currents, eix):
        """
        Determine whether a wound packet resurfaces.
        """
        RP = self.compute_return_potential(drop, tides, currents, eix)
        T = self.compute_threshold(tides)
        return RP > T, RP, T

    # ------------------------------------------------------------
    # QUEST GENERATION
    # ------------------------------------------------------------
    def generate_quest(self, drop, RP, T):
        """
        Turn a resurfaced wound into a quest object.
        """
        packet = drop.get("packet", {})
        sentence = packet.get("sentence", "...")

        return {
            "type": "wound_quest",
            "origin_sentence": sentence,
            "return_pressure": RP,
            "threshold": T,
            "meta": packet.get("meta", {}),
            "message": "An unresolved pattern resurfaces, seeking integration."
        }
