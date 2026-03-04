# ============================================================
# BirthForceOrgan — Party Atmosphere Edition
# ============================================================

class BirthForceOrgan:
    """
    Emits a 'birth force' packet when a new character is forming.
    Party-themed but fully Cathedral-physiology compliant.

    Expected behavior:
      - On tick, if a character_birth organ snapshot exists,
        emit a celebratory birth-force packet.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_name = None  # Prevents repeating the same birth event

    def tick(self):
        packets = []

        # Access other organ snapshots through the creature
        birth = self.creature.organs.get("character_birth")
        if not birth:
            return packets

        snap = birth.snapshot()
        name = snap.get("name")
        archetype = snap.get("archetype")

        # Only emit when a new name appears
        if name and name != self.last_name:
            self.last_name = name

            packets.append({
                "type": "birth_force",
                "name": name,
                "archetype": archetype,
                "celebration": "🎉 A new character enters the Cathedral!",
                "spark": "⚡",
            })

        return packets

    def snapshot(self):
        # Minimal snapshot for viewers
        return {
            "last_name": self.last_name
        }
