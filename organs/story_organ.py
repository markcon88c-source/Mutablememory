# ============================================================
# STORY ORGAN — NARRATIVE PHYSICS LAYER
# ============================================================

from organs.base_organ import BaseOrgan
from packet.story_packet import StoryPacket

class StoryOrgan(BaseOrgan):
    """
    Transforms meaning-level packets into story-level packets.
    This organ participates in narrative physics and feeds the
    EmergenceGateCathedral. It must use a zero-argument tick()
    to match the Cathedral heartbeat.
    """

    def __init__(self, creature):
        super().__init__()
        self.creature = creature
        self.inbox = []

    # --------------------------------------------------------
    # RECEIVE PACKETS
    # --------------------------------------------------------
    def receive(self, packet):
        self.inbox.append(packet)

    # --------------------------------------------------------
    # TICK — MUST TAKE ZERO ARGUMENTS
    # --------------------------------------------------------
    def tick(self):
        if not self.inbox:
            return None

        packet = self.inbox.pop(0)

        story_packet = StoryPacket(
            source="StoryOrgan",
            meaning=getattr(packet, "meaning", None),
            structure=getattr(packet, "structure", None),
            metadata={"narrative_force": 1.0}
        )

        self.bus.emit(story_packet)
        return story_packet
