#!/data/data/com.termux/files/usr/bin/python
# ============================================================
# SYMBOLIC PRESSURE MAIN SUPPORT
# Drives:
#   - Organ Bus
#   - Packet Bus
#   - Force Bus
#   - Symbolic Spark Organ
#   - Universal Viewer
# ============================================================

import time

# ------------------------------------------------------------
# FORCE-LOAD ALL ORGANS SO REGISTRIES FILL
# ------------------------------------------------------------
import organs.meaning_organ
import organs.sentence_builder_organ
import organs.pressures_organ
import organs.drift_organ
import organs.packet_bus_organ
import organs.force_bus_organ
import organs.symbolic_spark_organ

from organs.base_organ import BaseOrgan
from organs.packet_bus_organ import PacketBusOrgan
from organs.force_bus_organ import ForceBusOrgan
from organs.symbolic_spark_organ import SymbolicSparkOrgan


# ============================================================
# CREATURE
# ============================================================

class Creature:
    def __init__(self):
        self.organs = []
        self.last_packets = []
        self.forces = {}
        self.lastmeta = {}

        # Instantiate all BaseOrgan subclasses
        for cls in BaseOrgan.registry:
            organ = cls(self)
            self.organs.append(organ)

        # Explicit bus + symbolic organs
        self.packet_bus = PacketBusOrgan(self)
        self.force_bus = ForceBusOrgan(self)
        self.symbolic = SymbolicSparkOrgan(self)

    # --------------------------------------------------------
    # HEARTBEAT ORDER (CRITICAL)
    # --------------------------------------------------------
    def heartbeat(self):
        # 1. Run all organs FIRST
        for organ in self.organs:
            if hasattr(organ, "step"):
                organ.step()

        # 2. THEN run the buses
        self.packet_bus.step()
        self.force_bus.step()

        # 3. THEN symbolic
        self.symbolic.step()


# ============================================================
# VIEWERS
# ============================================================

def show_symbolic_view(creature):
    meta = getattr(creature, "lastmeta", {})
    symbolic = meta.get("symbolic", 0.0)
    spark_eff = meta.get("sparkeffective", 0.0)
    spark_after = meta.get("sparkafter", 0.0)

    print("==============================")
    print("=== 🔮 SYMBOLIC PRESSURE VIEW ===")
    print(f"🧠 Symbolic: {symbolic:.3f}")
    print(f"✨ Spark Effective: {spark_eff:.3f}")
    print(f"🌓 Spark After Symbolic: {spark_after:.3f}")
    print("🌱 Sub‑forces:")
    sub = meta.get("subforces", {})
    if sub:
        for k, v in sub.items():
            print(f"  {k}: {v}")
    else:
        print("  (none)")
    print("=================================")


def show_universal_viewer(creature):
    print()
    print("=== 🌐 UNIVERSAL VIEWER ===")

    print("🫀 METABOLIC BUS (Organs)")
    print("==========================")
    if creature.organs:
        for o in creature.organs:
            print(f"- {o.__class__.__name__}")
    else:
        print("(no organs)")

    print()
    print("📦 PACKET BUS (Packets)")
    print("========================")
    packets = getattr(creature, "last_packets", [])
    if packets:
        for i, p in enumerate(packets):
            print(f"[{i:02d}] {p}")
    else:
        print("(no packets)")

    print()
    print("⚡ FORCE BUS (Forces)")
    print("=====================")
    forces = getattr(creature, "forces", {})
    if forces:
        for k, v in forces.items():
            print(f"{k}: {v}")
    else:
        print("(no forces)")
    print("==============================")


# ============================================================
# MAIN LOOP
# ============================================================

def main():
    creature = Creature()

    while True:
        creature.heartbeat()
        show_symbolic_view(creature)
        show_universal_viewer(creature)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
