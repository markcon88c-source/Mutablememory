# ============================================================
# STM SPINE ORGAN — Cathedral Short-Term Memory Spine
# ============================================================

import random

class STMSpineOrgan:
    """
    STMSpineOrgan maintains a short-term memory spine for the Cathedral
    creature. It stores recent packets, provides rolling context, and
    participates in the metabolic pipeline.

    This version preserves the new physiology (tick(self, creature))
    while restoring legacy compatibility for CreatureCathedral, which
    still calls organ.tick() with zero arguments.
    """

    def __init__(self, creature):
        self.creature = creature

        # Rolling STM buffer
        self.buffer = []
        self.max_length = 32

        # Optional: last emitted STM frame
        self.last_frame = None

    # ============================================================
    # NEW PHYSIOLOGY — your real STM logic lives here
    # ============================================================
    def tick_core(self, creature):
        """
        New Cathedral physiology signature.
        Called once per heartbeat with the creature object.
        """

        # Pull last packet if available
        packet = getattr(creature, "last_packet", None)

        # Store packet in STM buffer
        if packet is not None:
            self.buffer.append(packet)
            if len(self.buffer) > self.max_length:
                self.buffer.pop(0)

        # Build STM frame
        frame = {
            "type": "stm_frame",
            "length": len(self.buffer),
            "recent": list(self.buffer[-5:])  # last 5 packets
        }

        self.last_frame = frame
        return {"stm": frame}

    # ============================================================
    # LEGACY COMPATIBILITY WRAPPER
    # ============================================================
    def tick(self):
        """
        CreatureCathedral calls organ.tick() with no arguments.
        Forward to tick_core(self.creature).
        """
        return self.tick_core(self.creature)

    # ============================================================
    # PIPELINE STEP — required by Cathedral metabolism
    # ============================================================
    def step(self, packet):
        """
        STMSpineOrgan does not modify packets in the pipeline.
        It only records them during tick().
        """
        return packet

    # ============================================================
    # SNAPSHOT — for viewer + state save
    # ============================================================
    def snapshot(self):
        return {
            "buffer": list(self.buffer),
            "last_frame": self.last_frame
        }
