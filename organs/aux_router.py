# organs/aux_router.py

class AuxRouter:
    """
    AUXILIARY ROUTER (DECOUPLER)
    ----------------------------
    This organ does NOT route, mutate, or interpret packets.
    Its ONLY job is to provide a clean handoff point so that
    new viewers can be built without touching metabolic code.

    It acts as a buffer:
        Flow2 → AuxRouter → (any viewer you want)
    """

    def __init__(self, creature):
        self.creature = creature

    def handoff(self, packets):
        """
        Accept packets and return them unchanged.
        This allows new viewers to attach here with zero dependencies.
        """

        print("\n🟧 AUX ROUTER (DECOUPLER)")
        print("──────────────────────────────")
        print(f"Received {len(packets)} packets.")
        print("→ Passing packets to next viewer (no metabolic dependencies).")

        return packets
