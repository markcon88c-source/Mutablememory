from packets import narrative_packet

class NarrativeOrgan:
    def __init__(self, bus):
        self.bus = bus

    def tick(self):
        packets = self.bus.packets
        if not packets:
            return None

        latest = packets[-1]

        # Only transform sentence packets
        if latest.get("type") != "sentence":
            return None

        text = latest.get("sentence", "")

        # Minimal narrative transformation
        narrative = f"NARRATIVE: {text}"

        return narrative_packet(narrative)
