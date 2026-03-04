#!/data/data/com.termux/files/usr/bin/python
# ============================================================
# ORGAN ONLINE VIEWER
# Shows which organs produced packets or forces this heartbeat.
# ============================================================

def show_organ_online(creature):
    print("=== 🧬 ORGAN ONLINE STATUS ===")
    print("==============================")

    packets = getattr(creature, "last_packets", [])
    forces  = getattr(creature, "forces", {})

    # --------------------------------------------------------
    # Build lookup tables
    # --------------------------------------------------------
    packet_sources = set()
    force_sources  = set()

    # Packet source detection
    for p in packets:
        src = p.get("meta", {}).get("organ")
        if src:
            packet_sources.add(src)

    # Force source detection
    if isinstance(forces, dict):
        src = forces.get("source")
        if src:
            force_sources.add(src)

    # --------------------------------------------------------
    # Print organ status
    # --------------------------------------------------------
    for organ in creature.organs:
        name = organ.__class__.__name__

        if name in packet_sources:
            print(f"{name:25} 🟢 packets")
        elif name in force_sources:
            print(f"{name:25} 🟢 forces")
        else:
            print(f"{name:25} 🟡 idle")

    print("==============================")
