# STORY VIEWER — 20 tubes showing story-type attraction + ascension + stability

class StoryViewer:
    def __init__(self):
        self.last_sentence = None
        self.last_type = None
        self.last_forces = None
        self.last_ascension = None
        self.last_stability = None

        # 20 story-type tubes
        self.tubes = [
            "myth", "quest", "conflict", "revelation", "tragedy",
            "comedy", "ritual", "origin", "return", "threshold",
            "storm", "ocean", "memory", "identity", "drift",
            "pressure", "union", "fracture", "ascent", "descent"
        ]

    def accept(self, packet):
        if packet.get("type") == "story":
            payload = packet["payload"]

            # Expecting:
            # {
            #   "sentence": "...",
            #   "type": "quest",
            #   "forces": {"storm":0.2,"primal":0.1,...},
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.last_sentence = payload.get("sentence", "")
            self.last_type = payload.get("type", "unknown")
            self.last_forces = payload.get("forces", {})
            self.last_ascension = payload.get("ascension", 0)
            self.last_stability = payload.get("stability", 0)

    def render(self):
        if self.last_sentence is None:
            return "[StoryViewer] …awaiting story seed…"

        # Stability → emoji
        stability_map = {
            0: "🟥",
            1: "🟨",
            2: "🟩",
            3: "💚",
        }
        icon = stability_map.get(self.last_stability, "🟨")

        # Ascension height (0–3)
        asc_map = {
            0: "·",     # ground
            1: "─",     # low rise
            2: "╱╲",    # mid ascent
            3: "⟰",     # emerald ascension
        }
        asc_symbol = asc_map.get(self.last_ascension, "·")

        # Build 20 tubes
        lines = []
        for tube in self.tubes:
            marker = " "  # empty tube
            if tube == self.last_type:
                marker = asc_symbol  # sentence appears here

            # Light force influence (just a nudge)
            force_val = self.last_forces.get(tube, 0)
            if force_val > 0.15:
                marker = marker + "*"
            elif force_val > 0.05:
                marker = marker + "·"

            lines.append(f"{tube:10} | {marker}")

        tubes_block = "\n".join(lines)

        return (
            f"[StoryViewer {icon}] Story‑type attraction\n"
            f"Sentence: “{self.last_sentence}”\n"
            f"Ascension: {asc_symbol}\n"
            f"{tubes_block}"
        )
