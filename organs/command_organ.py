# COMMAND ORGAN — placeholder for command bus integration

class CommandOrgan:
    def __init__(self, bus):
        self.bus = bus

    def accept(self, packet):
        # For now, this organ does not consume any packets
        pass

    def tick(self):
        # No command output yet
        return None
