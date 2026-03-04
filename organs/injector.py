from typing import List, Dict, Any

class Injector:
    """
    Cathedral Injector — BusSink for UniversalBusOrgan.

    Routing modes:
    - broadcast: send every packet to every organ
    - directed: use packet["target"] or packet["channel"]
    - selective: only send to registered organs
    """

    def __init__(self, creature, receptacle):
        self.creature = creature
        self.receptacle = receptacle
        self.buffer: List[Dict[str, Any]] = []

        self.mode = "broadcast"
        self.selective_map = {}

    def handle_bus_packet(self, packet: Dict[str, Any]) -> None:
        if packet is not None:
            self.buffer.append(packet)

    def set_mode(self, mode: str) -> None:
        if mode in ("broadcast", "directed", "selective"):
            self.mode = mode

    def register(self, channel: str, organ) -> None:
        self.selective_map.setdefault(channel, []).append(organ)

    def flush(self) -> List[Dict[str, Any]]:
        if not self.buffer:
            return []

        packets = self.buffer[:]
        self.buffer.clear()
        delivered = []

        for packet in packets:
            channel = packet.get("channel")
            target = packet.get("target")

            if self.mode == "broadcast":
                for organ in self.creature.organs.values():
                    self.receptacle.accept({"organ": organ, "packet": packet})
                delivered.append(packet)

            elif self.mode == "directed":
                if target and target in self.creature.organs:
                    organ = self.creature.organs[target]
                    self.receptacle.accept({"organ": organ, "packet": packet})
                    delivered.append(packet)
                elif channel and channel in self.creature.organs:
                    organ = self.creature.organs[channel]
                    self.receptacle.accept({"organ": organ, "packet": packet})
                    delivered.append(packet)

            elif self.mode == "selective":
                if channel in self.selective_map:
                    for organ in self.selective_map[channel]:
                        self.receptacle.accept({"organ": organ, "packet": packet})
                    delivered.append(packet)

        return delivered
