from organs.base_organ import BaseOrgan

class NozzleOrgan(BaseOrgan):
    def __init__(self, creature):
        super().__init__(creature)
        self.name = "NozzleOrgan"

        # Channel → creature attribute name
        self.ROUTES = {
            "character": "meaning",
            "faction": "meaning",
            "word": "builder",
            "sentence": "builder",
        }

    def accept(self, packet):
        # 1. Explicit target routing (if injector or bus sets packet["target"])
        target = packet.get("target")
        if target:
            organ = getattr(self.creature, target, None)
            if organ:
                # Prefer step() if available, fallback to handle_bus_packet()
                if hasattr(organ, "step"):
                    return organ.step(packet)
                if hasattr(organ, "handle_bus_packet"):
                    return organ.handle_bus_packet(packet)
            return packet

        # 2. Channel-based routing
        channel = packet.get("channel")
        if channel in self.ROUTES:
            organ_name = self.ROUTES[channel]
            organ = getattr(self.creature, organ_name, None)

            if organ:
                if hasattr(organ, "step"):
                    return organ.step(packet)
                if hasattr(organ, "handle_bus_packet"):
                    return organ.handle_bus_packet(packet)

        # 3. Default: return unchanged
        return packet
