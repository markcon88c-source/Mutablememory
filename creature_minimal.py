# creature_minimal.py
# ============================================================
# MINIMAL CREATURE FOR SENTENCE BUS DEBUGGING
# Only includes:
#   - PacketBusOrgan
#   - BasePacketSource registry (SentenceBuilderOrgan)
# ============================================================

from organs.packet_bus_organ import PacketBusOrgan

class CreatureMinimal:
    def __init__(self):
        # Only the packet bus — no meaning organ, no forces, no symbolic
        self.packet_bus = PacketBusOrgan(self)

        # Storage for packets
        self.last_packets = []
