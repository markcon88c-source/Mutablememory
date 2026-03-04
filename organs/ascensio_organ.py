class AscensioOrgan:
    def __init__(self, command_bus, force_bus, packet_bus):
        self.packet_bus = packet_bus
        force_bus.add_listener(self.receive_block)

        self.levels = 11
        self.micro_gates = 17

    def receive_block(self, block):
        self.advance(block)
        self.emit_packet(block)

    def advance(self, block):
        if block.ascended:
            return

        block.micro_gate += 1
        if block.micro_gate >= self.micro_gates:
            block.micro_gate = 0
            block.level += 1

        if block.level >= self.levels:
            block.ascended = True
            block.level = self.levels
            block.micro_gate = self.micro_gates - 1

    def emit_packet(self, block):
        packet = {
            "type": "ascensio",
            "word": block.word,
            "level": block.level,
            "micro_gate": block.micro_gate,
            "ascended": block.ascended
        }
        self.packet_bus.emit(packet)
