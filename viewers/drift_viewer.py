# DRIFT VIEWER — shows drift direction, intensity, waves, spikes, and ascension

class DriftViewer:
    def __init__(self):
        self.direction = "flat"     # "up", "down", "flat"
        self.intensity = 0.0        # 0.0–1.0
        self.reason = None          # text reason
        self.spike = 0.0            # spike magnitude
        self.wave = 0.0             # wave magnitude
        self.ascension = 0          # 0–3
        self.stability = 0          # 0–3

    def accept(self, packet):
        if packet.get("type") == "drift":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "direction": "up/down/flat",
            #   "intensity": 0.0–1.0,
            #   "reason": "...",
            #   "spike": 0.0–1.0,
            #   "wave": 0.0–1.0,
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.direction = payload.get("direction", self.direction)
            self.intensity = payload.get("intensity", self.intensity)
            self.reason = payload.get("reason", self.reason)
            self.spike = payload.get("spike", self.spike)
            self.wave = payload.get("wave", self.wave)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        # No drift yet
        if self.reason is None:
            return "[DriftViewer] …awaiting drift…"

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

        # Drift direction arrow
        if self.direction == "up":
            arrow = "↑"
        elif self.direction == "down":
            arrow = "↓"
        else:
            arrow = "→"

        # Drift intensity bar
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

        intensity_bar = bar(self.intensity)
        spike_bar = bar(self.spike)
        wave_bar = bar(self.wave)

        # Drift wave graph (fun part)
        wave_graph = ""
        if self.wave > 0.6:
            wave_graph = "≈≈≈≈≈≈≈"
        elif self.wave > 0.3:
            wave_graph = "≈≈≈≈"
        elif self.wave > 0.1:
            wave_graph = "≈≈"
        else:
            wave_graph = "·"

        # Drift spike graph
        spike_graph = ""
        if self.spike > 0.6:
            spike_graph = "⚡⚡⚡"
        elif self.spike > 0.3:
            spike_graph = "⚡⚡"
        elif self.spike > 0.1:
            spike_graph = "⚡"
        else:
            spike_graph = "·"

        return (
            f"[DriftViewer {icon}] Drift field\n"
            f"Ascension: {asc_symbol}\n"
            f"Direction: {arrow} ({self.direction})\n"
            f"Intensity: {intensity_bar} ({self.intensity:.2f})\n"
            f"Wave:      {wave_bar} ({self.wave:.2f})   {wave_graph}\n"
            f"Spike:     {spike_bar} ({self.spike:.2f})   {spike_graph}\n"
            f"Reason: {self.reason}"
        )
