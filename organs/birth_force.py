# ============================================================
# BIRTH FORCE ORGAN — CATHEDRAL BIRTH CEREMONY
# Combines NameHeart identity + Character Sheet into a
# single birth event with initialized Cathedral forces.
# ============================================================

import random

class BirthForceOrgan:
    """
    Performs the Cathedral birth ceremony:
    - waits for NameHeart identity packets
    - waits for CharacterFactory character sheets
    - fuses them into a newborn being
    - initializes Cathedral force signatures
    - emits a 'birth' packet
    """

    def __init__(self, creature):
        self.creature = creature

        # Buffers
        self.pending_identity = None
        self.pending_character = None

        # Newborns
        self.newborns = []

    # --------------------------------------------------------
    # Modern Cathedral compatibility wrapper
    # --------------------------------------------------------
    def tick(self, creature):
        return self.tick_legacy()

    # --------------------------------------------------------
    # RECEIVE PACKETS
    # --------------------------------------------------------
    def receive_packet(self, packet):
        ptype = packet.get("type")

        # Identity from NameHeartOrgan
        if ptype == "character_idea":
            self.pending_identity = packet

        # Character sheet from HeartCharacterFactory
        if ptype == "character_sheet":
            self.pending_character = packet

        # If both are present, perform birth
        if self.pending_identity and self.pending_character:
            self.perform_birth()

    # --------------------------------------------------------
    # BIRTH CEREMONY
    # --------------------------------------------------------
    def perform_birth(self):
        identity = self.pending_identity
        sheet = self.pending_character.get("payload", {})

        name = sheet.get("name", "Unnamed")
        role = sheet.get("role", "wanderer")
        seed = sheet.get("seed", "")

        # Cathedral force initialization
        newborn_forces = {
            "pulse": random.randint(1, 5),
            "tone": random.randint(1, 5),
            "spark": random.randint(1, 5),
            "drift": random.randint(1, 5),
            "echo": random.randint(1, 5),
            "chaos": random.randint(0, 3),
            "clarity": random.randint(0, 3),
            "memory": random.randint(0, 3),
            "pressure": random.randint(1, 4),
            "cluster": f"cluster-{random.randint(100,999)}",
        }

        newborn = {
            "name": name,
            "role": role,
            "seed": seed,
            "forces": newborn_forces,
            "stats": sheet.get("stats", {}),
            "origin_name": sheet.get("origin_name", ""),
            "alignment": sheet.get("alignment", "Neutral Neutral"),
        }

        self.newborns.append(newborn)

        # Clear buffers
        self.pending_identity = None
        self.pending_character = None

        # Emit birth packet
        self.creature.universal_bus.emit(
            source="birth_force",
            channel="identity",
            kind="birth",
            payload=newborn
        )

    # --------------------------------------------------------
    # LEGACY TICK — emit most recent newborn if needed
    # --------------------------------------------------------
    def tick_legacy(self):
        if not self.newborns:
            return

        self.creature.universal_bus.emit(
            source="birth_force",
            channel="identity",
            kind="newborn_echo",
            payload=self.newborns[-1]
        )
