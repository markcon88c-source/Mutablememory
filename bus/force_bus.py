class ForceBus:
    def __init__(self):
        self.listeners = []

    def add_listener(self, fn):
        self.listeners.append(fn)

    def emit(self, block):
        for fn in self.listeners:
            fn(block)
