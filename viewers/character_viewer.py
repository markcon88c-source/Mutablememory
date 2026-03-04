# CHARACTER VIEWER — shows the young character with light force influence + ascension band

class CharacterViewer:
    def __init__(self):
        self.name = None
        self.role = None
        self.seed = None
        self.stats = {}
        self.forces = {}
        self.ascension = 0
        self.stability = 0

    def accept(self, packet):
        ptype = packet.get("type")

        # Birth packet
        if ptype == "character_birth":
            payload = packet["payload"]
            self.name = payload.get("name")
            self.seed = payload.get("seed")

        # Sheet packet
        elif ptype == "character_sheet":
            payload = packet["payload"]
            self.role = payload.get("role")
            self.stats = payload.get("stats", {})

        # Forces packet (light influence)
        elif ptype == "character_forces":
            self.forces = packet.get("payload", {})

        # Identity packet (ascension + stability may come from here)
        elif ptype == "identity":
            ident = packet.get("payload", {})
            self.ascension = ident.get("ascension", self.ascension)
            self.stability = ident.get("stability", self.stability)

    def render(self):
        if self.name is None:
            return "[CharacterViewer] …awaiting first character…"

        # Stability → emoji
        stability_map = {
            0: "🟥",
            1: "🟨",
            2: "🟩",
            3: "💚",
        }
        icon = stability_map.get(self.stability, "🟨")

        # Ascension height
        asc_map = {
            0: "·",
            1: "─",
            2: "╱╲",
            3: "⟰",
        }
        asc_symbol = asc_map.get(self.ascension, "·")

        # Light force influence (just a nudge)
        force_lines = []
        for k, v in self.forces.items():
            if v > 0.15:
                mark = "*"
            elif v > 0.05:
                mark = "·"
            else:
                mark = " "
            force_lines.append(f"{k:10} | {mark}")

        forces_block = "\n".join(force_lines) if force_lines else "none"

        # Stats block
        stats_block = ", ".join(f"{k}:{v}" for k, v in self.stats.items()) if self.stats else "none"

        return (
            f"[CharacterViewer {icon}] {self.name}\n"
            f"Role: {self.role}\n"
            f"Seed: {self.seed}\n"
            f"Ascension: {asc_symbol}\n"
            f"Stats: {stats_block}\n"
            f"Forces:\n{forces_block}"
        )
