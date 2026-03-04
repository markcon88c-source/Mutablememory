# sentence_bus_viewer.py
# ============================================================
# SIMPLE SENTENCE BUS VIEWER
# Shows only SentenceBuilder packets and PacketBus packets.
# ============================================================

def show_sentence_bus(creature):
    print("=== 📝 SENTENCE BUS VIEWER ===")

    # SentenceBuilder output
    packets = getattr(creature, "last_packets", [])

    if not packets:
        print("(no sentence packets)")
    else:
        for i, p in enumerate(packets):
            if p.get("type") == "sentence":
                print(f"[{i:02}] {p}")

    print("==============================")
