# ============================================================
# INJECTOR ORGAN — Cathedral wrapper around the core Injector
# ============================================================

from dataclasses import dataclass
from typing import Any, Dict, List

from bus.injector import Injector


@dataclass
class InjectorStats:
    total_packets: int = 0
    last_batch_size: int = 0


class InjectorOrgan:
    """
    Cathedral InjectorOrgan
    - Wraps the core bus.injector.Injector
    - Drains the UniversalBus each heartbeat
    - Delivers packets to receptive organs
    - Exposes simple stats for viewers/diagnostics
    """

    def __init__(self, creature):
        self.creature = creature
        self.name = "InjectorOrgan"

        # Core injector (new system)
        self.injector = Injector()

        # Simple stats
        self.stats = InjectorStats()

    # --------------------------------------------------------
    # Heartbeat entrypoint
    # --------------------------------------------------------
    def tick(self):
        """
        Called each creature heartbeat.
        Drains the bus and injects packets into organs.
        """
        bus = getattr(self.creature, "bus", None)
        if bus is None:
            return

        # Drain packets from the unified bus
        packets = bus.drain()
        self.stats.last_batch_size = len(packets)
        self.stats.total_packets += len(packets)

        if not packets:
            return

        # Deliver via core injector
        self.injector.inject(self.creature, packets)

    # --------------------------------------------------------
    # Optional: snapshot for viewers
    # --------------------------------------------------------
    def snapshot(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "total_packets": self.stats.total_packets,
            "last_batch_size": self.stats.last_batch_size,
        }
