# run_sentence_bus.py
# ============================================================
# SENTENCE BUS TEST HARNESS (ISOLATED)
# Does NOT depend on Creature having a bus.
# Creates its own PacketBus and SentenceBuilderOrgan.
# ============================================================

import time

from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.base_packet_source import BasePacketSource
from organs.base_organ import BaseOrgan

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
# Minimal Creature Stub (NO CHANGES TO REAL CREATURE)
# ------------------------------------------------------------
class TestCreature:
    def __init__(self):
        self.bus = PacketBus()
        self.organs = [
            SentenceBuilderOrgan(self)
        ]


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
def main():
    creature = TestCreature()

    print("=== 📝 SENTENCE BUS VIEWER ===")

    while True:
        # Feed the organ a simple thought
        thought = {
            "words": ["the", "creature", "is", "alive"]
        }

        # Step only real organs
        for organ in creature.organs:
            if hasattr(organ, "step"):
                organ.step(thought, {}, {}, {})

        # Collect sentence packets
        packets = creature.bus.collect("sentence")

        if packets:
            for p in packets:
                print(f"[sentence] {p['data']['text']}")
        else:
            print("(no sentence packets)")

        print("==============================")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
