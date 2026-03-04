# NARRATIVE VIEWER — shows the early story-attractor the sentence is closest to

class NarrativeViewer:
    def __init__(self):
        self.last_type = None
        self.last_sentence = None
        self.last_stability = None

    def accept(self, packet):
        if packet.get("type") == "narrative":
            payload = packet["payload"]

            # Expecting:
            # {
            #   "sentence": "...",
            #   "type": "myth / quest / conflict / revelation / etc",
            #   "stability": 0–3
            # }
            self.last_sentence = payload.get("sentence", "")
            self.last_type = payload.get("type", "unknown")
            self.last_stability = payload.get("stability", 0)

    def render(self):
        if self.last_type is None:
            return "[NarrativeViewer] …awaiting narrative seed…"

        # Stability → emoji
        stability_map = {
            0: "🟥",  # unstable
            1: "🟨",  # forming
            2: "🟩",  # stable
            3: "💚",  # emerald ascension
        }
        icon = stability_map.get(self.last_stability, "🟨")

        # Display the narrative attractor
        return (
            f"[NarrativeViewer {icon}] "
            f"Story‑type: {self.last_type}\n"
            f"    ↳ from: “{self.last_sentence}”"
        )
