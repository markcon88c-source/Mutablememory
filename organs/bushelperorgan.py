
# ============================================================
# BusHelperOrgan — Cathedral Organ
# ============================================================

class BusHelperOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.energy = 1.0
        self.pressure = 0.0
        self.cycle = 0

    def tick(self):
        # Metabolic cycle
        self.cycle += 1
        self.energy *= 0.99
        self.pressure = (self.cycle % 20) / 20.0

        # Emit symbolic packet
        self.bus.emit(
            source="BusHelperOrgan",
            channel="bushelperorgan",
            kind="symbolic",
            payload={
                "cycle": self.cycle,
                "energy": round(self.energy, 3),
                "pressure": round(self.pressure, 3),
                "signature": "BusHelperOrgan_sig"
            }
        )
