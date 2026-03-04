# STM GRAVITY VIEWER — shows memory gravity wells formed from ocean clumps

class STMGravityViewer:
    def __init__(self):
        self.wells = []          # memory wells (clusters)
        self.ascension = 0
        self.stability = 0

    def accept(self, packet):
        if packet.get("type") == "stm_gravity":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "wells": [
            #       {"id": "W1", "mass": 0.42, "sentences": ["S12","S14"], "pull": 0.18},
            #       ...
            #   ],
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.wells = payload.get("wells", [])
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        if not self.wells:
            return "[STMGravityViewer] …awaiting memory gravity…"

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

        # Build gravity well display
        lines = []
        for w in self.wells:
            wid = w.get("id", "?")
            mass = w.get("mass", 0)
            pull = w.get("pull", 0)
            sents = w.get("sentences", [])

            # Mass → visual weight
            if mass > 0.6:
                mass_bar = "███"
            elif mass > 0.3:
                mass_bar = "██"
            else:
                mass_bar = "█"

            # Pull → gravitational arrow
            if pull > 0.2:
                pull_icon = "⬇⬇"
            elif pull > 0.1:
                pull_icon = "⬇"
            else:
                pull_icon = "·"

            sent_list = ", ".join(sents) if sents else "(none)"

            lines.append(
                f"{wid:4} | mass:{mass_bar} pull:{pull_icon} | {sent_list}"
            )

        wells_block = "\n".join(lines)

        return (
            f"[STMGravityViewer {icon}] Memory gravity wells\n"
            f"Ascension: {asc_symbol}\n"
            f"{wells_block}"
        )
