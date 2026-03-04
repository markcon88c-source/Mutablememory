# IDENTITY VIEWER — shows the character growing into their identity

class IdentityViewer:
    def __init__(self):
        self.name = None
        self.role = None
        self.traits = {}
        self.faction_pull = {}
        self.ascension = 0
        self.stability = 0
        self.stage = "seedling"   # seedling → forming → emerging → defined

    def accept(self, packet):
        if packet.get("type") == "identity":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "name": "...",
            #   "role": "...",
            #   "traits": {"bravery":0.3,"curiosity":0.6,...},
            #   "faction_pull": {"storm":0.2,"primal":0.4,...},
            #   "ascension": 0–3,
            #   "stability": 0–3,
            #   "stage": "seedling/forming/emerging/defined"
            # }
            self.name = payload.get("name", self.name)
            self.role = payload.get("role", self.role)
            self.traits = payload.get("traits", self.traits)
            self.faction_pull = payload.get("faction_pull", self.faction_pull)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)
            self.stage = payload.get("stage", self.stage)

    def render(self):
        if self.name is None:
            return "[IdentityViewer] …awaiting identity seed…"

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

        # Trait bar
        def bar(v):
            if v > 0.75:
                return "████"
            elif v > 0.5:
                return "███"
            elif v > 0.25:
                return "██"
            elif v > 0.1:
                return "█"
            else:
                return "·"

        # Build traits block
        trait_lines = []
        for k, v in self.traits.items():
            trait_lines.append(f"{k:10} | {bar(v)} ({v:.2f})")
        traits_block = "\n".join(trait_lines) if trait_lines else "none"

        # Build faction pull block
        pull_lines = []
        for k, v in self.faction_pull.items():
            pull_lines.append(f"{k:10} | {bar(v)} ({v:.2f})")
        pull_block = "\n".join(pull_lines) if pull_lines else "none"

        return (
            f"[IdentityViewer {icon}] Character identity growth\n"
            f"Ascension: {asc_symbol}\n"
            f"Stage: {self.stage}\n"
            f"Name: {self.name}\n"
            f"Role: {self.role}\n\n"
            f"Traits:\n{traits_block}\n\n"
            f"Faction Pull:\n{pull_block}"
        )
