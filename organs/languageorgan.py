class LanguageOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.cycle = 0

    def tick(self):
        self.cycle += 1
        self.bus.emit(
            source="LanguageOrgan",
            channel="language",
            kind="language",
            payload={"cycle": self.cycle}
        )
