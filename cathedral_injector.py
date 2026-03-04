# ============================================================
# CATHEDRAL INJECTOR — Full Cathedral-Compatible Injector
# ============================================================

from typing import List, Dict, Any


class CathedralInjector:
    """
    Cathedral Injector used by CreatureCathedral.
    This class must:
    - accept packets from organs (via handle_bus_packet)
    - buffer them
    - deliver them to the CathedralReceptacle
    - support tick() with NO arguments
    - support tick_core(creature) for Cathedral metabolism
    """

    def __init__(self, creature):
        self.creature = creature
        self.buffer: List[Dict[str, Any]] = []
        self.mode = "broadcast"
        self.selective_map = {}

    # ------------------------------------------------------------
    # Accept packets from organs
    # ------------------------------------------------------------
    def handle_bus_packet(self, packet: Dict[str, Any]):
        self.buffer.append(packet)

    # ------------------------------------------------------------
    # Mode control
    # ------------------------------------------------------------
    def set_mode(self, mode: str):
        self.mode = mode

    def register_selective(self, channel: str, organ_name: str):
        self.selective_map[channel] = organ_name

    # ------------------------------------------------------------
    # NEW PHYSIOLOGY — real injector logic
    # ------------------------------------------------------------
    def tick_core(self, creature):
        """
        Deliver exactly one packet per heartbeat.
        """
        if not self.buffer:
            return None

        packet = self.buffer.pop(0)

        # Selective routing
        if self.mode == "selective":
            channel = packet.get("channel")
            if channel in self.selective_map:
                packet["target"] = self.selective_map[channel]

        # Deliver to CathedralReceptacle
        return creature.receptacle.accept(packet)

    # ------------------------------------------------------------
    # LEGACY COMPATIBILITY WRAPPER
    # CreatureCathedral calls injector.tick() with NO arguments
    # ------------------------------------------------------------
    def tick(self):
        return self.tick_core(self.creature)
