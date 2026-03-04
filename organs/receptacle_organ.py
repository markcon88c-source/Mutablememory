from typing import List, Dict, Any

class ReceptacleOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.queue: List[Dict[str, Any]] = []

    def accept(self, packet: Dict[str, Any]) -> None:
        if packet is not None:
            self.queue.append(packet)

    def accept_many(self, packets: List[Dict[str, Any]]) -> None:
        for p in packets or []:
            self.accept(p)

    def pull(self) -> List[Dict[str, Any]]:
        if not self.queue:
            return []
        out = self.queue[:]
        self.queue.clear()
        return out
