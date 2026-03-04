# Organs_Narrative_General_Gravity.py

class NarrativeGravityOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.current_gravity = {
            "magnitude": 0.0,
            "zone": None,
            "stability": 0.3,
            "attempts_since_green": 0,
            "chaos": 0.0,
            "storm": 0.0,
            "drift": "steady water",
        }

    def step(self):
        # Pull packets from the universal bus
        packets = self.bus.read_all()

        # Basic gravity metabolism
        chaos = 0.0
        storm = 0.0

        for p in packets:
            if hasattr(p, "force"):
                chaos += p.force * 0.01
                storm += p.force * 0.005

        # Update gravity field
        self.current_gravity["chaos"] = chaos
        self.current_gravity["storm"] = storm

        # Stability
        stability = self.current_gravity["stability"]
        stability = stability + (chaos * 0.1) - (storm * 0.05)
        if stability < 0.0:
            stability = 0.0
        if stability > 1.0:
            stability = 1.0
        self.current_gravity["stability"] = stability

        # Zone
        if stability > 0.75:
            zone = "GREEN"
        elif stability > 0.45:
            zone = "BLUE"
        elif stability > 0.25:
            zone = "YELLOW"
        else:
            zone = "RED"

        prev_zone = self.current_gravity["zone"]
        self.current_gravity["zone"] = zone

        # Attempts since last GREEN
        if zone == "GREEN":
            self.current_gravity["attempts_since_green"] = 0
        else:
            self.current_gravity["attempts_since_green"] += 1

        # Drift
        if chaos < 0.05:
            drift = "steady water"
        elif chaos < 0.15:
            drift = "slow tide"
        else:
            drift = "rough current"

        self.current_gravity["drift"] = drift

    def get_field(self):
        return self.current_gravity
