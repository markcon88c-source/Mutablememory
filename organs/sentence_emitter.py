from packets import sentence_packet

class SentenceEmitter:
    def __init__(self, bus):
        self.bus = bus

    def tick(self):
        packets = self.bus.packets
        if not packets:
            return None

        latest = packets[-1]

        # Accept language packets only
        if latest.get("type") != "language":
            return None

        text = latest.get("text", "")

        return sentence_packet(text)
