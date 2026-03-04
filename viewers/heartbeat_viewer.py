# HEARTBEAT VIEWER — shows the creature's pulse, rhythm, waveform, and ascension

class HeartbeatViewer:
    def __init__(self):
        self.rate = 0.0            # beats per second (normalized 0–1)
        self.strength = 0.0        # how strong the beat is (0–1)
        self.wave = 0.0            # waveform amplitude (0–1)
        self.packets = 0           # packets processed this beat
        self.ascension = 0         # 0–3
        self.stability = 0         # 0–3
        self.beat_id = 0           # increments each beat

    def accept(self, packet):
        if packet.get("type") == "heartbeat":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "rate": 0.0–1.0,
            #   "strength": 0.0–1.0,
            #   "wave": 0.0–1.0,
            #   "packets": int,
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.rate = payload.get("rate", self.rate)
            self.strength = payload.get("strength", self.strength)
            self.wave = payload.get("wave", self.wave)
            self.packets = payload.get("packets", self.packets)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)
            self.beat_id += 1

    def render(self):
        if self.beat_id == 0:
            return "[HeartbeatViewer] …awaiting first heartbeat…"

        # Stability → emoji
        stability_map = {
            0: "🟥",
            1: "🟨",
            2: "🟩",
            3: "💚",
        }
        icon = stability_map.get(self.stability, "🟨")

        # Ascension pulse height
        asc_map = {
            0: "·",
            1: "─",
            2: "╱╲",
            3: "⟰",
        }
        asc_symbol = asc_map.get(self.ascension, "·")

        # Bar helper
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

        # Waveform (fun part)
        if self.wave > 0.7:
            wave_graph = "♥♥♥♥♥"
        elif self.wave > 0.4:
            wave_graph = "♥♥♥"
        elif self.wave > 0.1:
            wave_graph = "♥"
        else:
            wave_graph = "·"

        return (
            f"[HeartbeatViewer {icon}] Beat {self.beat_id}\n"
            f"Ascension Pulse: {asc_symbol}\n"
            f"Rate:     {bar(self.rate)} ({self.rate:.2f})\n"
            f"Strength: {bar(self.strength)} ({self.strength:.2f})\n"
            f"Waveform: {bar(self.wave)} ({self.wave:.2f})   {wave_graph}\n"
            f"Packets this beat: {self.packets}"
        )
