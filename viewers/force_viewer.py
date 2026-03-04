# FORCE VIEWER — shows conversion between primal and storm forces

class ForceViewer:
    def __init__(self):
        self.storm = 0.0
        self.primal = 0.0
        self.drift = 0.0
        self.pressure = 0.0
        self.exchange = 0.0   # how much storm <-> primal conversion
        self.ascension = 0
        self.stability = 0

    def accept(self, packet):
        if packet.get("type") == "forces":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "storm": 0.0–1.0,
            #   "primal": 0.0–1.0,
            #   "drift": 0.0–1.0,
            #   "pressure": 0.0–1.0,
            #   "exchange": 0.0–1.0,
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.storm = payload.get("storm", self.storm)
            self.primal = payload.get("primal", self.primal)
            self.drift = payload.get("drift", self.drift)
            self.pressure = payload.get("pressure", self.pressure)
            self.exchange = payload.get("exchange", self.exchange)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        # No data yet
        if self.storm == 0 and self.primal == 0 and self.drift == 0 and self.pressure == 0:
            return "[ForceViewer] …awaiting force data…"

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

        storm_bar = bar(self.storm)
        primal_bar = bar(self.primal)
        drift_bar = bar(self.drift)
        pressure_bar = bar(self.pressure)
        exch_bar = bar(self.exchange)

        return (
            f"[ForceViewer {icon}] Storm ↔ Primal conversion\n"
            f"Ascension: {asc_symbol}\n"
            f"Storm:    {storm_bar}  ({self.storm:.2f})\n"
            f"Primal:   {primal_bar}  ({self.primal:.2f})\n"
            f"Drift:    {drift_bar}  ({self.drift:.2f})\n"
            f"Pressure: {pressure_bar}  ({self.pressure:.2f})\n"
            f"Exchange: {exch_bar}  ({self.exchange:.2f})"
        )
