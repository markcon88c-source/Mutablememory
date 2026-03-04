# organs/substrate_engine.py
# ============================================================
# SUBSTRATE ENGINE — narrative-force field for packet existence
# ============================================================

from typing import Dict, Any, List
import math


class SubstrateEngine:
    """
    The Substrate Engine is the medium packets exist in.
    It is a narrative-force field composed of:

      • narrative gravity (meaning mass curvature)
      • story density (compression of meaning)
      • temporal pull (future-bending force)
      • symbolic charge (archetypal resonance)
      • chaos turbulence (mobility + disturbance)
      • wound gravity (collapsed narrative mass)
      • archetype wells (stable attractors)
      • tension field (unresolved meaning pressure)

    Every packet has a substrate state.
    Every heartbeat updates the substrate field.
    """

    def __init__(self, creature):
        self.creature = creature

        # Global narrative fields
        self.field = {
            "gravity": 0.0,
            "tension": 0.0,
            "story_density": 0.0,
            "temporal_pull": 0.0,
            "symbolic_charge": 0.0,
            "chaos_turbulence": 0.0,
            "wound_gravity": 0.0,
            "archetype_pull": 0.0,
        }

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def update(self, packets: List[Dict[str, Any]]) -> None:
        """
        Update the substrate field based on all packets in the ocean.
        This is the heart of the substrate engine.
        """

        if not packets:
            self._reset_field()
            return

        # Aggregate forces
        gravities = []
        tensions = []
        densities = []
        temporal = []
        symbolic = []
        chaos = []
        wounds = []
        archetypes = []

        for drop in packets:
            packet = drop.get("packet", {})
            meta = packet.get("meta", {})

            # Meaning mass → narrative gravity
            stability = meta.get("stability", 0.0)
            gravities.append(stability)

            # Unresolved meaning → tension
            weird = meta.get("weirdness", 0.0)
            drift = meta.get("drift_metrics", {}).get("value", 0.0)
            fracture = meta.get("fracture", 0.0)
            tensions.append(abs(drift) + weird + fracture)

            # Compression of meaning → story density
            symbolic_val = packet.get("symbolic", 0.0)
            densities.append(symbolic_val)

            # Future pull → temporal pull
            acceleration = meta.get("acceleration", 0.0)
            temporal.append(acceleration)

            # Archetypal resonance → symbolic charge
            symbolic_charge = packet.get("symbolic", 0.0)
            symbolic.append(symbolic_charge)

            # Mobility + disturbance → chaos turbulence
            chaos_val = packet.get("chaos", 0.0)
            chaos.append(chaos_val)

            # Collapsed narrative mass → wound gravity
            energy = drop.get("energy", 0.5)
            wounds.append(1.0 - energy)

            # Deep stable packets → archetype wells
            if drop.get("depth", 0) >= 2:
                archetypes.append(stability)

        # Compute field values
        self.field["gravity"] = self._avg(gravities)
        self.field["tension"] = self._avg(tensions)
        self.field["story_density"] = self._avg(densities)
        self.field["temporal_pull"] = self._avg(temporal)
        self.field["symbolic_charge"] = self._avg(symbolic)
        self.field["chaos_turbulence"] = self._avg(chaos)
        self.field["wound_gravity"] = self._avg(wounds)
        self.field["archetype_pull"] = self._avg(archetypes)

    def apply_to_packet(self, packet: Dict[str, Any]) -> None:
        """
        Update a packet's substrate state based on the global field.
        """

        packet["substrate"] = {
            "gravity": self.field["gravity"],
            "tension": self.field["tension"],
            "story_density": self.field["story_density"],
            "temporal_pull": self.field["temporal_pull"],
            "symbolic_charge": self.field["symbolic_charge"],
            "chaos_turbulence": self.field["chaos_turbulence"],
            "wound_gravity": self.field["wound_gravity"],
            "archetype_pull": self.field["archetype_pull"],
        }

    def get_field(self) -> Dict[str, float]:
        return self.field

    # ------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------
    def _avg(self, arr: List[float]) -> float:
        if not arr:
            return 0.0
        return sum(arr) / len(arr)

    def _reset_field(self):
        for k in self.field:
            self.field[k] = 0.0

