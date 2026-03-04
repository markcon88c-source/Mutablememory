# STM INTEGRITY VIEWER — shows how forces compress, stretch, and stabilize STM

class STMIntegrityViewer:
    def __init__(self):
        self.compression = 0.0
        self.cohesion = 0.0
        self.shear = 0.0
        self.tension = 0.0
        self.ascension = 0
        self.stability = 0

    def accept(self, packet):
        if packet.get("type") == "stm_integrity":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "compression": 0.0–1.0,
            #   "cohesion": 0.0–1.0,
            #   "shear": 0.0–1.0,
            #   "tension": 0.0–1.0,
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.compression = payload.get("compression", self.compression)
            self.cohesion = payload.get("cohesion", self.cohesion)
            self.shear = payload.get("shear", self.shear)
            self.tension = payload.get("tension", self.tension)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        # No data yet
        if self.compression == 0 and self.cohesion == 0 and self.shear == 0 and self.tension == 0:
            return "[STMIntegrityViewer] …awaiting STM integrity data…"

        # Stability → emoji
        stability_map = {
            0: "🟥",  # unstable
            1: "🟨",  # forming
            2: "🟩",  # stable
            3: "💚",  # emerald ascension
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

        # Convert force values into bars
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

        comp_bar = bar(self.compression)
        coh_bar = bar(self.cohesion)
        shear_bar = bar(self.shear)
        tension_bar = bar(self.tension)

        return (
            f"[STMIntegrityViewer {icon}] STM structural forces\n"
            f"Ascension: {asc_symbol}\n"
            f"Compression: {comp_bar}  ({self.compression:.2f})\n"
            f"Cohesion:    {coh_bar}  ({self.cohesion:.2f})\n"
            f"Shear:       {shear_bar}  ({self.shear:.2f})\n"
            f"Tension:     {tension_bar}  ({self.tension:.2f})"
        )
