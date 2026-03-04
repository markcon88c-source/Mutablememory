# ============================================================
#  QUEST EQUATION PACKET – v1.0 (Canonical, Immutable)
#  A standardized, persistent, cross-organ symbolic packet.
#
#  Once created, a QuestEquationPacket:
#    - never mutates
#    - never changes interpretation
#    - never changes wound tag
#    - never changes signature
#    - is passed through every organ intact
#
#  This is the mythic mathblock lineage object.
# ============================================================

import hashlib
import random


class QuestEquationPacket:
    @staticmethod
    def build(glyph, forces):
        """
        Build a canonical quest equation packet from:
          - glyph (A–Z + Ø)
          - forces (spark, drift, echo, chaos, clarity, memory, pressure)

        This packet is immutable and standardized across all organs.
        """

        # ----------------------------------------------------
        # 1. Generate symbolic equation (glyph-based)
        # ----------------------------------------------------
        # These are symbolic, not algebraic — narrative math.
        eq = QuestEquationPacket._generate_symbolic_equation(glyph, forces)

        # ----------------------------------------------------
        # 2. Generate interpretation (meaning block)
        # ----------------------------------------------------
        interp = QuestEquationPacket._interpret(eq, forces)

        # ----------------------------------------------------
        # 3. Assign wound type (mythic wound taxonomy)
        # ----------------------------------------------------
        wound = QuestEquationPacket._assign_wound(forces)

        # ----------------------------------------------------
        # 4. Memory key (for quest machines)
        # ----------------------------------------------------
        memory_key = f"{glyph}:{wound}:{hash(eq) % 99999}"

        # ----------------------------------------------------
        # 5. Canonical signature (immutable identity)
        # ----------------------------------------------------
        signature = QuestEquationPacket._signature(eq, interp, wound)

        # ----------------------------------------------------
        # 6. Final immutable packet
        # ----------------------------------------------------
        return {
            "equation": eq,
            "interpretation": interp,
            "wound": wound,
            "memory_key": memory_key,
            "signature": signature,
        }

    # ========================================================
    #  INTERNAL HELPERS
    # ========================================================

    @staticmethod
    def _generate_symbolic_equation(glyph, forces):
        """
        Create a symbolic quest equation using glyph + forces.
        These are mythic equations, not algebraic ones.
        """

        # Pick two force names to combine
        force_names = list(forces.keys())
        f1, f2 = random.sample(force_names, 2)

        # Symbolic form
        return f"{glyph} = {f1} ⊕ {f2}"

    @staticmethod
    def _interpret(eq, forces):
        """
        Generate a narrative interpretation of the symbolic equation.
        """

        # Pick a force to anchor the meaning
        dominant = max(forces, key=lambda k: forces[k])

        interpretations = {
            "spark": "A call to ignite beginnings.",
            "drift": "A sign of shifting paths.",
            "echo": "A memory returning from the deep.",
            "chaos": "A wound of instability seeking form.",
            "clarity": "A moment of insight breaking through.",
            "memory": "A forgotten truth resurfacing.",
            "pressure": "A burden demanding release.",
        }

        return interpretations.get(dominant, "A symbolic transformation.")

    @staticmethod
    def _assign_wound(forces):
        """
        Assign a mythic wound type based on force distribution.
        """

        if forces["chaos"] > 0.6:
            return "instability_wound"
        if forces["clarity"] < 0.2:
            return "confusion_wound"
        if forces["memory"] < 0.2:
            return "forgetting_wound"
        if forces["drift"] > 0.5:
            return "misalignment_wound"

        return "balance_wound"

    @staticmethod
    def _signature(eq, interp, wound):
        """
        Create an immutable signature for the packet.
        """

        raw = f"{eq}|{interp}|{wound}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
