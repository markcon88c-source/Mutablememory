# IDENTITY ORGAN — integrates birth, sheet, and forces into a living identity

from packets import identity_packet

class IdentityOrgan:
    def __init__(self, bus):
        self.bus = bus
        self.identity = {
            "name": None,
            "role": None,
            "seed": None,
            "stats": {},
            "forces": {},
        }

    def accept(self, packet):
        ptype = packet.get("type")

        # Birth layer
        if ptype == "character_birth":
            payload = packet["payload"]
            self.identity["name"] = payload.get("name")
            self.identity["seed"] = payload.get("seed")

        # Sheet layer
        elif ptype == "character_sheet":
            payload = packet["payload"]
            self.identity["role"] = payload.get("role")
            self.identity["stats"] = payload.get("stats", {})

        # Forces layer
        elif ptype == "character_forces":
            self.identity["forces"] = packet["payload"]

    def tick(self):
        # Emit identity every tick
        return identity_packet(self.identity)
