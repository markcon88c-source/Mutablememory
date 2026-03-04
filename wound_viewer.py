# viewer/wound_viewer.py
# ============================================================
# WOUND VIEWER — resurfacing, return pressure, quests
# ============================================================

from typing import Any, Dict, List


class WoundViewer:
    """
    Visualizes:
      • abyss wounds (drops)
      • return potential (RP) vs threshold (T)
      • which wounds resurface
      • the quests they generate
      • ocean soundscape context
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
        abyss: List[Dict[str, Any]] = ocean_state.get("abyss", [])
        tides = ocean_state.get("tides", {})
        currents = ocean_state.get("currents", {})

        sound = self.ocean.get_soundscape()

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🌑 WOUND VIEWER — abyss, return pressure, quests")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self._show_soundscape(sound)

        if not abyss:
            print("\nNo abyss wounds yet. The ocean is quiet.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            return

        print(f"\nAbyss wounds: {len(abyss)}")
        print("--------------------------------------------------------")

        resurfaced_quests = []

        for idx, drop in enumerate(abyss):
            packet = drop.get("packet", {})
            sentence = packet.get("sentence", "...").strip()
            meta = packet.get("meta", {})

            # You can compute EIX however you like; for now, pull from meta
            eix = meta.get("EIX", {
                "Phi": meta.get("strangeness", 0.0),
                "Omega": meta.get("acceleration", 0.0),
            })

            # Depth is implicit here: abyss = 3
            drop.setdefault("depth", 3)

            should, RP, T = self.wounds.should_resurface(
                drop=drop,
                tides=tides,
                currents=currents,
                eix=eix,
            )

            status = "🌊 RESURFACES" if should else "⚫ STAYS BELOW"
            bar = self._bar(RP, T)

            print(f"\n[{idx+1}] {status}")
            print(f"Sentence: {sentence or '…'}")
            print(f"RP (return potential): {RP:.3f}")
            print(f"T  (threshold):        {T:.3f}")
            print(f"Depth: {drop.get('depth', 3)}   Energy: {drop.get('energy', 0.5):.3f}")
            print(f"Bar: {bar}")

            if should:
                quest = self.wounds.generate_quest(drop, RP, T)
                resurfaced_quests.append(quest)
                print("→ Quest formed:")
                print(f"   Type: {quest['type']}")
                print(f"   Message: {quest['message']}")

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if resurfaced_quests:
            print(f"Total quests this cycle: {len(resurfaced_quests)}")
        else:
            print("No quests formed this cycle — wounds remain submerged.")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    def _show_soundscape(self, sound: Dict[str, Any]) -> None:
        mode = sound.get("mode", "calm")
        intensity = sound.get("intensity", 0.0)
        texture = sound.get("texture", "smooth")
        layers = sound.get("layers", {})

        print(f"\n🌊 Ocean Soundscape")
        print(f"Mode:      {mode}")
        print(f"Intensity: {intensity:.3f}")
        print(f"Texture:   {texture}")
        print(
            f"Layers: surface={layers.get('surface', 0)}, "
            f"mid={layers.get('mid', 0)}, "
            f"deep={layers.get('deep', 0)}, "
            f"abyss={layers.get('abyss', 0)}"
        )

    def _bar(self, RP: float, T: float, width: int = 24) -> str:
        """
        Visual bar: left = threshold, right = RP.
        """
        RP_clamped = max(0.0, min(RP, 1.2))
        T_clamped = max(0.0, min(T, 1.2))

        rp_pos = int((RP_clamped / 1.2) * width)
        t_pos = int((T_clamped / 1.2) * width)

        chars = []
        for i in range(width):
            if i == t_pos:
                chars.append("|")  # threshold marker
            elif i <= rp_pos:
                chars.append("█")
            else:
                chars.append("░")
        return "".join(chars)
