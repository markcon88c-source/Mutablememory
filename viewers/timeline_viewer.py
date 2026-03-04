# TIMELINE VIEWER — first viewer for factions, showing their timeline + ascension

class TimelineViewer:
    def __init__(self):
        self.entries = []       # list of timeline events
        self.ascension = 0      # 0–3
        self.stability = 0      # 0–3

    def accept(self, packet):
        if packet.get("type") == "timeline":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "entries": [
            #       {"faction":"storm","influence":0.3,"time":12},
            #       {"faction":"primal","influence":0.5,"time":12},
            #       ...
            #   ],
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.entries = payload.get("entries", self.entries)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        if not self.entries:
            return "[TimelineViewer] …awaiting faction timeline…"

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

        # Influence bar
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

        # Build timeline lines
        lines = []
        for e in self.entries:
            faction = e.get("faction", "?")
            influence = e.get("influence", 0)
            time = e.get("time", "?")
            lines.append(f"t={time:3} | {faction:10} | {bar(influence)} ({influence:.2f})")

        timeline_block = "\n".join(lines)

        return (
            f"[TimelineViewer {icon}] Faction timeline\n"
            f"Ascension: {asc_symbol}\n"
            f"{timeline_block}"
        )
