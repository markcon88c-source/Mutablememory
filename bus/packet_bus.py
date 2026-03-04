class PacketBus:
    def __init__(self):
        self.listeners = []

    def add_listener(self, fn):
        self.listeners.append(fn)

    def emit(self, packet):
        for fn in self.listeners:
            fn(packet)
