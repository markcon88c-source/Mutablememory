# MEANING VIEWER — displays meaning packets on the wall

class MeaningViewer:
    def __init__(self):
        self.last_meaning = None

    def accept(self, packet):
        if packet.get("type") == "meaning":
            self.last_meaning = packet["payload"]

    def render(self):
        if self.last_meaning is None:
            return "[MeaningViewer] No meaning yet."
        return f"[MeaningViewer] {self.last_meaning}"
