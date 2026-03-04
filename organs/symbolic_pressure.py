# SYMBOLIC PRESSURE ORGAN — CATHEDRAL EDITION
# Computes symbolic pressure from packets, forces, and narrative signals.
# Feeds into ReservoirOrgan and ForceBusOrgan.

class SymbolicPressureOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.pressure = 0.0
        self.decay_rate = 0.92
        self.amplify = 1.35

    def tick(self):
        # Pull packets from the creature’s last cycle
        packets = getattr(self.creature, "last_packets", [])

        # Decay old pressure
        self.pressure *= self.decay_rate

        # Add new symbolic pressure from packets
        for p in packets:
            if not isinstance(p, dict):
                continue

            # Force score contributes directly
            fs = p.get("force_score", 0.0)
            self.pressure += fs * 0.15

            # Named characters add identity pressure
            if "full_name" in p:
                self.pressure += 0.25

            # World‑related packets add narrative mass
            if p.get("packet_type") == "world":
                self.pressure += 0.4

        # Clamp to reasonable range
        if self.pressure < 0:
            self.pressure = 0.0
        if self.pressure > 100:
            self.pressure = 100.0

        # Expose to creature state
        self.creature.state["symbolic_pressure"] = self.pressure

    def get_pressure(self):
        return self.pressure
