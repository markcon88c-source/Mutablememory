# PRESSURE ORGAN — maintains and emits narrative pressure

from packets import pressure_packet

class PressureOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.pressure = 1  # baseline pressure

    def accept(self, packet):
        ptype = packet.get("type")

        # Increase pressure
        if ptype == "pressure_increase":
            self.pressure += packet["payload"].get("amount", 1)

        # Decrease pressure
        elif ptype == "pressure_decrease":
            self.pressure -= packet["payload"].get("amount", 1)
            if self.pressure < 0:
                self.pressure = 0

    def tick(self):
        return pressure_packet({"value": self.pressure})
