# PRESSURE VIEWER — reads pressure across the 7 forces + primal

class PressureViewer:
    def __init__(self):
        self.pressures = {}     # storm, primal, drift, memory, identity, ocean, gravity, etc.
        self.total = 0.0
        self.ascension = 0
        self.stability = 0

    def accept(self, packet):
        if packet.get("type") == "pressure_field":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "pressures": {"storm":0.2,"primal":0.3,"drift":0.1,...},
            #   "total": 0.0–1.0,
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.pressures = payload.get("pressures", self.pressures)
            self.total = payload.get("total", self.total)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        if not self.pressures:
            return "[PressureViewer] …awaiting pressure field…"

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

        # Convert pressure values into bars
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

        # Build pressure lines
        lines = []
        for k, v in self.pressures.items():
            lines.append(f"{k:10} | {bar(v)} ({v:.2f})")

        pressures_block = "\n".join(lines)

        total_bar = bar(self.total)

        return (
            f"[PressureViewer {icon}] Global pressure field\n"
            f"Ascension: {asc_symbol}\n"
            f"Total Pressure: {total_bar} ({self.total:.2f})\n"
            f"{pressures_block}"
        )
