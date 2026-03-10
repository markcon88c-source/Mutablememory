
# ============================================================
# UNIVERSAL BUS — Cathedral v3
# Emits Cathedral packets and heartbeat signals
# ============================================================

class UniversalBus:
    def __init__(self, creature):
        self.creature = creature
        self.registry = {}

    # --------------------------------------------------------
    # REGISTER ORGANS
    # --------------------------------------------------------
    def register(self, name, organ):
        self.registry[name] = organ

    # --------------------------------------------------------
    # EMIT PACKETS INTO THE BLOODSTREAM
    # --------------------------------------------------------
    def emit(self, packet):
        # Debug: show every packet entering the bloodstream
        print("[BUS] packet →", packet)

        # Deliver to all organs
        for organ in self.registry.values():
            try:
                organ.receive(packet)
            except Exception as e:
                print("[BUS] organ receive error:", e)

    # --------------------------------------------------------
    # HEARTBEAT — drives the entire Cathedral metabolism
    # --------------------------------------------------------
    def tick(self):

        # 1) Emit lexical_tick signal for LexicalOrgan
        self.emit({
            "source": "bus",
            "channel": "lexical",
            "kind": "tick",
            "payload": {}
        })

        # 2) Tick all organs
        for organ in self.registry.values():
            try:
                organ.tick()
            except Exception as e:
                print("[BUS] organ tick error:", e)
