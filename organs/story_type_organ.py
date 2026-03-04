# ============================================================
# STORY TYPE ORGAN — FORCE-SIGNATURE CLASSIFIER
# ============================================================
# Reads the 3‑word window from SentenceBuilderOrgan and
# classifies it into a story-type attractor based on force
# signatures (spark, drift, pressure, clarity, echo).
#
# Emits:
#   channel="story_type"
#   payload={
#       "sentence": "...",
#       "story_type": "...",
#       "confidence": float,
#       "forces": {...},
#       "iteration": int
#   }
# ============================================================

class StoryTypeOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.last_sentence = ""
        self.last_story_type = "neutral"
        self.iteration = 0

        # Force signatures for first exposure
        self.force_map = {
            "calm":     {"drift": 0.8, "spark": 0.2, "pressure": 0.1},
            "quiet":    {"drift": 0.7, "spark": 0.1, "pressure": 0.1},
            "soft":     {"drift": 0.6, "spark": 0.2, "pressure": 0.1},

            "fire":     {"spark": 0.9, "pressure": 0.7, "drift": 0.1},
            "burn":     {"spark": 0.8, "pressure": 0.6, "drift": 0.1},
            "storm":    {"pressure": 0.9, "spark": 0.6, "drift": 0.1},

            "light":    {"spark": 0.7, "clarity": 0.8, "echo": 0.5},
            "bright":   {"spark": 0.6, "clarity": 0.7, "echo": 0.4},
            "dream":    {"drift": 0.9, "echo": 0.7, "clarity": 0.2},

            "walk":     {"drift": 0.5, "spark": 0.4, "clarity": 0.3},
            "path":     {"drift": 0.6, "spark": 0.3, "clarity": 0.3},
            "road":     {"drift": 0.5, "spark": 0.3, "clarity": 0.4},
        }

        # Map force signatures to story types
        self.story_map = {
            "calm":     "calm",
            "quiet":    "calm",
            "soft":     "calm",

            "fire":     "chaos",
            "burn":     "chaos",
            "storm":    "chaos",

            "light":    "mythic",
            "bright":   "mythic",
            "dream":    "dream",

            "walk":     "adventure",
            "path":     "adventure",
            "road":     "adventure",
        }

    # --------------------------------------------------------
    # BUS HANDLER — listens for 3‑word sentence packets
    # --------------------------------------------------------
    def handle_bus_packet(self, packet):
        if packet["channel"] != "sentence":
            return
        self.last_sentence = packet["payload"]

    # --------------------------------------------------------
    # RUN — classify the 3‑word window into a story type
    # --------------------------------------------------------
    def run(self):
        if not self.last_sentence:
            return

        self.iteration += 1
        words = self.last_sentence.lower().split()

        # Default neutral field
        story_type = "neutral"
        confidence = 0.2
        forces = {"spark": 0.1, "drift": 0.1, "pressure": 0.1, "clarity": 0.1, "echo": 0.1}

        # Scan each word for force signatures
        for w in words:
            if w in self.force_map:
                forces = self.force_map[w]
                story_type = self.story_map.get(w, "neutral")
                confidence = 0.8
                break

        self.last_story_type = story_type

        # Emit story-type packet
        self.creature.universal_bus.emit(
            source="story_type",
            channel="story_type",
            kind="story_type_state",
            payload={
                "sentence": self.last_sentence,
                "story_type": story_type,
                "confidence": confidence,
                "forces": forces,
                "iteration": self.iteration,
            }
        )
