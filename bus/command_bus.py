# command_bus.py

class CommandBus:
    def __init__(self):
        self.listeners = {}

    def register(self, verb, callback):
        if verb not in self.listeners:
            self.listeners[verb] = []
        self.listeners[verb].append(callback)

    def emit(self, packet):
        verb = packet.get("verb")
        if verb in self.listeners:
            for cb in self.listeners[verb]:
                cb(packet)
