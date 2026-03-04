# ============================================================
# HEART CHARACTER FACTORY — CATHEDRAL CHARACTER SHEET FORGE
# Builds full D&D-style character sheets from NameHeart packets
# and Cathedral force signatures.
# ============================================================

import random

class HeartCharacterFactory:
    """
    Converts NameHeartOrgan identity packets + Cathedral forces
    into full character sheets. Emits a complete character
    object each tick.
    """

    def __init__(self, creature):
        self.creature = creature
        self.characters = []

    # --------------------------------------------------------
    # RECEIVE PACKETS (unchanged)
    # --------------------------------------------------------
    def receive_packet(self, packet):
        if packet.get("type") != "character_idea":
            return

        base = packet.get("base")
        mutated = packet.get("mutated")
        role = packet.get("role")
        seed = packet.get("seed")

        if not mutated:
            return

        # Pull Cathedral forces if available
        forces = getattr(self.creature, "forces", None)
        if forces:
            pulse = forces.get("pulse", 1)
            tone = forces.get("tone", 1)
            cluster = forces.get("cluster", "")
            spark = forces.get("spark", 1)
            drift = forces.get("drift", 1)
            echo = forces.get("echo", 1)
            chaos = forces.get("chaos", 0)
            clarity = forces.get("clarity", 0)
            memory = forces.get("memory", 0)
            pressure = forces.get("pressure", 1)
        else:
            pulse = tone = spark = drift = echo = pressure = 1
            chaos = clarity = memory = 0
            cluster = ""

        # ----------------------------------------------------
        # DERIVED STATS (D&D-style)
        # ----------------------------------------------------
        strength = pulse + random.randint(1, 4)
        will = tone + clarity + random.randint(1, 4)
        insight = echo + memory + random.randint(1, 4)
        presence = spark + drift + random.randint(1, 4)
        luck = max(1, 10 - chaos + random.randint(-1, 2))

        # ----------------------------------------------------
        # ALIGNMENT (based on forces)
        # ----------------------------------------------------
        if clarity > chaos:
            moral = "Lawful"
        elif chaos > clarity:
            moral = "Chaotic"
        else:
            moral = "Neutral"

        if pulse > tone:
            ethic = "Good"
        elif tone > pulse:
            ethic = "Evil"
        else:
            ethic = "Neutral"

        alignment = f"{moral} {ethic}"

        # ----------------------------------------------------
        # BUILD CHARACTER SHEET
        # ----------------------------------------------------
        character = {
            "name": mutated,
            "origin_name": base,
            "role": role,
            "seed": seed,
            "alignment": alignment,

            "forces": {
                "pulse": pulse,
                "tone": tone,
                "cluster": cluster,
                "spark": spark,
                "drift": drift,
                "echo": echo,
                "chaos": chaos,
                "clarity": clarity,
                "memory": memory,
                "pressure": pressure,
            },

            "stats": {
                "strength": strength,
                "will": will,
                "insight": insight,
                "presence": presence,
                "luck": luck,
            }
        }

        self.characters.append(character)

        # Keep memory bounded
        if len(self.characters) > 50:
            self.characters = self.characters[-50:]

    # ========================================================
    # NEW PHYSIOLOGY — your real tick logic (renamed)
    # ========================================================
    def tick_core(self, creature):
        """
        Cathedral metabolism:
        - creature calls: organ.tick(self)
        - we return a packet
        - injector + bus handle routing
        """
        if not self.characters:
            return None

        char = self.characters[-1]

        return {
            "source": "character_factory",
            "channel": "identity",
            "kind": "character_sheet",
            "payload": char,
        }

    # ========================================================
    # LEGACY COMPATIBILITY WRAPPER
    # CreatureCathedral calls organ.tick() with NO arguments
    # ========================================================
    def tick(self):
        return self.tick_core(self.creature)
