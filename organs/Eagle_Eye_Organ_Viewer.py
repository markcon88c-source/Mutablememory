class Organ:
    name: str

    def forward_map(self, packet):
        # read-only interpretation of a packet
        return packet

    def reverse_map(self, packet):
        # read-only reverse interpretation
        return packet
