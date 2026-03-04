# viewer/ocean_space_viewer.py
# ============================================================
# OCEAN SPACE VIEWER — the living in‑memory ocean habitat
# ============================================================

from typing import Any, Dict, List
import math


class OceanSpaceViewer:
    """
    The Ocean Space Viewer visualizes the ocean as a *place*:
      • packet clusters (schools)
      • drift flows (currents)
      • chaos plumes (turbulence)
      • symbolic reefs (stable structures)
      • wound swarms (abyssal gatherings)
      • storms (surface churn)
      • deep pressure zones
      • resurfacing bubbles

    This is not a log.
    This is a habitat.
    """

    def __init__(self, creature):
        self.creature = creature
        self.ocean = creature.sentence_ocean
        self.wounds = creature.wound_organ

    # --------------------------------------------------------
    # Public entrypoint
    # --------------------------------------------------------
    def show(self) -> None:
        ocean_state = self.ocean.ocean

        surface = ocean_state["surface"]
        mid = ocean_state["mid"]
        deep = ocean_state["deep"]
        abyss = ocean_state["abyss"]

        tides = ocean_state["tides"]
        storms = ocean_state["storms"]
        currents = ocean_state["currents"]

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🌊 OCEAN SPACE VIEWER — living subconscious habitat")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        self._show_ocean_header(tides, storms, currents)
        self._show_layer("Surface", surface, icon="🌤️", depth=0)
        self._show_layer("Mid‑Water", mid, icon="🌊", depth=1)
        self._show_layer("Deep Water", deep, icon="🌑", depth=2)
        self._show_abyss(abyss, tides, currents)

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # --------------------------------------------------------
    # Layer displays
    # --------------------------------------------------------
    def _show_layer(self, name: str, drops: List[Dict[str, Any]], icon: str, depth: int):
        print(f"\n{icon} {name} — {len(drops)} packets")
        print("--------------------------------------------------------")

        if not drops:
            print("  (empty)")
            return

        for drop in drops[:8]:  # show first 8 for readability
            packet = drop["packet"]
            sentence = packet.get("sentence", "...").strip()
            chaos = packet.get("chaos", 0.0)
            drift = packet.get("drift", 0.0)
            symbolic = packet.get("symbolic", 0.0)

            print(f"• {sentence}")
            print(f"    chaos={chaos:.2f}  drift={drift:.2f}  symbolic={symbolic:.2f}")

    # --------------------------------------------------------
    # Abyss (wound habitat)
    # --------------------------------------------------------
    def _show_abyss(self, abyss, tides, currents):
        print(f"\n🌑 Abyss — {len(abyss)} wounds")
        print("--------------------------------------------------------")

        if not abyss:
            print("  (quiet abyss)")
            return

        for drop in abyss[:8]:
            packet = drop["packet"]
            sentence = packet.get("sentence", "...").strip()

            meta = packet.get("meta", {})
            eix = meta.get("EIX", {
                "Phi": meta.get("strangeness", 0.0),
                "Omega": meta.get("acceleration", 0.0),
            })

            should, RP, T = self.wounds.should_resurface(
                drop=drop,
                tides=tides,
                currents=currents,
                eix=eix,
            )

            status = "🌫️ drifting" if not should else "🌋 rising"

            print(f"• {sentence}")
            print(f"    RP={RP:.3f}  T={T:.3f}  status={status}")

    # --------------------------------------------------------
    # Ocean header (weather)
    # --------------------------------------------------------
    def _show_ocean_header(self, tides, storms, currents):
        print("\n🌫️ Ocean Weather")
        print(f"  Drift Current:    {tides['drift_current']:.3f}")
        print(f"  Chaos Current:    {tides['chaos_current']:.3f}")
        print(f"  Symbolic Current: {tides['symbolic_current']:.3f}")

        if storms["active"]:
            print(f"  Storm:            {storms['type']} ({storms['intensity']:.2f})")
        else:
            print("  Storm:            none")

        print(f"  Gravity Well:     {currents['gravity_well']:.3f}")
        print(f"  Weirdness Flow:   {currents['weirdness_flow']:.3f}")
