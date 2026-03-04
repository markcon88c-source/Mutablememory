# run_force_bus.py
# ============================================================
# FORCE BUS TEST HARNESS (ISOLATED)
# Tests ForceBuilderOrgan + PacketBus + ForceViewer
# ============================================================

import time

from organs.force_builder_organ import ForceBuilderOrgan
from organs.force_viewer import ForceViewer


# ------------------------------------------------------------
# Minimal PacketBus for testing
# ------------------------------------------------------------
class PacketBus:
    def __init__(self):
        self._packets = []

    def send(self, packet):
        self._packets.append(packet)

    def collect(self, packet_type):
        out = [p for p in self._packets if p["type"] == packet_type]
        self._packets = []
        return out


# ------------------------------------------------------------
# Minimal Creature Stub
# ------------------------------------------------------------
class TestCreature:
    def __init__(self):
        self.bus = PacketBus()
        self.organs = [
            ForceBuilderOrgan(self),
            ForceViewer(self)
        ]


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
def main():
    creature = TestCreature()

    print("=== 💥 FORCE BUS VIEWER ===")

    while True:
        # Feed the organ a simple force input
        thought = {
            "forces": {
                "semantic_pull": 0.4,
                "reservoir_push": 0.2,
                "drift": -0.1
            }
        }

        # Step all organs
        for organ in creature.organs:
            if hasattr(organ, "step"):
                organ.step(thought, {}, {}, {})

        # Collect force packets
        packets = creature.bus.collect("force")

        if packets:
            for p in packets:
                print(f"[force] {p['data']}")
        else:
            print("(no force packets)")

        print("==============================")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
