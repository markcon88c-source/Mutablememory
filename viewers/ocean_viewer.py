# OCEAN VIEWER — 20 tubes showing sentence interactions in the ocean

class OceanViewer:
    def __init__(self):
        self.frames = []      # recent ocean packets
        self.interactions = {}  # clumps, bonds, repulsions, turbulence

        # 20 ocean tubes (depth bands)
        self.tubes = [
            "surface", "foam", "spray", "crest", "eddy",
            "drift", "shoal", "sway", "pull", "curl",
            "undertow", "sink", "deep", "abyss", "rift",
            "vent", "shadow", "pressure", "trench", "core"
        ]

    def accept(self, packet):
        if packet.get("type") == "ocean_view":
            payload = packet.get("payload", {})
            # Expecting:
            # {
            #   "sentences": [ {id, depth, drift, ascension, stability}, ... ],
            #   "interactions": {clumps:[], bonds:[], repulsions:[], turbulence:[]}
            # }
            self.frames = payload.get("sentences", [])
            self.interactions = payload.get("interactions", {})

    def render(self):
        if not self.frames:
            return "[OceanViewer] …awaiting ocean activity…"

        # Stability → emoji
        stability_map = {
            0: "🟥",
            1: "🟨",
            2: "🟩",
            3: "💚",
        }

        # Ascension height
        asc_map = {
            0: "·",
            1: "─",
            2: "╱╲",
            3: "⟰",
        }

        # Build tube display
        tube_lines = []
        for tube in self.tubes:
            # find sentences whose depth matches this tube
            contents = []
            for s in self.frames:
                if s.get("depth") == tube:
                    stab = stability_map.get(s.get("stability", 0), "🟨")
                    asc = asc_map.get(s.get("ascension", 0), "·")
                    contents.append(f"{stab}{asc}{s.get('id')}")

            if contents:
                joined = " ".join(contents)
            else:
                joined = ""

            tube_lines.append(f"{tube:10} | {joined}")

        tubes_block = "\n".join(tube_lines)

        # Interaction block
        def fmt(label, key, emoji):
            pairs = self.interactions.get(key, [])
            if not pairs:
                return f"{label}: (none)"
            lines = [f"{emoji} {a} ↔ {b}" for a, b in pairs]
            return f"{label}:\n  " + "\n  ".join(lines)

        clump_block = fmt("Clumping", "clumps", "🧲")
        bond_block = fmt("Bonding", "bonds", "🔗")
        rep_block = fmt("Repulsion", "repulsions", "🌀")
        turb_block = fmt("Turbulence", "turbulence", "🌪️")

        return (
            f"[OceanViewer 🌊] Sentence interactions in the ocean\n"
            f"{tubes_block}\n\n"
            f"{clump_block}\n"
            f"{bond_block}\n"
            f"{rep_block}\n"
            f"{turb_block}"
        )
