class SentenceOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.cycle = 0

    def tick(self):
        self.cycle += 1
        self.bus.emit(
            source="SentenceOrgan",
            channel="sentence",
            kind="sentence",
            payload={"cycle": self.cycle}
        )
