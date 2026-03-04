# organs/heart_character.py

class HeartCharacter:
    """
    Unified identity object built from:
      - NameHeart packet (true identity)
      - Old CharacterFactory (mythic/proto flavor)
    """

    def __init__(self, packet, mythic, proto):
        # -----------------------------
        # TRUE IDENTITY (from NameHeart)
        # -----------------------------
        self.full_name = packet.get("full_name")
        self.seed = packet.get("seed")
        self.block_id = packet.get("block_id")
        self.letters = packet.get("letters")
        self.mode = packet.get("mode")
        self.force_type = packet.get("force")
        self.cluster = packet.get("cluster")
        self.pulse = packet.get("pulse")
        self.tone = packet.get("tone")
        self.origin_block_id = packet.get("origin_block_id")
        self.parent_block_ids = packet.get("parent_block_ids")

        # -----------------------------
        # FLAVOR NAMES (from old system)
        # -----------------------------
        self.mythic = mythic
        self.proto = proto

        # -----------------------------
        # UNIFIED FORCE DERIVATION
        # -----------------------------
        self.forces = self.derive_forces()

        # -----------------------------
        # QUEST FIELDS (empty for now)
        # -----------------------------
        self.wounds = []
        self.quests = []

    # -----------------------------------------------------
    # FORCE DERIVATION
    # -----------------------------------------------------
    def derive_forces(self):
        """
        Creates a unified force profile from pulse, tone, and cluster.
        """
        spark = self.pulse
        drift = self.tone
        echo = (self.pulse + self.tone) / 2

        chaos = self.cluster.count("W")
        clarity = self.cluster.count("U")
        memory = self.cluster.count("A")

        pressure = self.pulse * self.tone

        return {
            "spark": spark,
            "drift": drift,
            "echo": echo,
            "chaos": chaos,
            "clarity": clarity,
            "memory": memory,
            "pressure": pressure,
            "type": self.force_type,
        }
