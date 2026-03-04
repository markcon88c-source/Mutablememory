# ============================================================
# BRUSH-UP ORGAN — EMERALD EXPRESSIVE EDITION
# ------------------------------------------------------------
# Receives a sentence, generates refinement candidates, scores
# them, and emits a brush-up packet for the viewer.
# ============================================================

class BrushUpOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.cycle = 0
        self.last_packet = None

    # --------------------------------------------------------
    # BUS HANDLER — receives sentence packets
    # --------------------------------------------------------
    def handle_bus_packet(self, packet):
        if packet["channel"] != "sentence":
            return

        sentence = packet["payload"]
        self.process_sentence(sentence)

    # --------------------------------------------------------
    # MAIN PROCESSING
    # --------------------------------------------------------
    def process_sentence(self, sentence):
        self.cycle += 1

        # Basic candidate variations
        candidates = [
            sentence,
            " ".join(reversed(sentence.split())),
            sentence.capitalize(),
            f"{sentence} ✨",
            f"💚 {sentence} 💚",
            f"{sentence} — flicker 🌱",
        ]

        # Simple scoring
        scores = [
            1.0,
            0.4,
            0.7,
            0.63,
            0.72,
            0.4,
        ]

        emerald = int(20 + (self.cycle % 10))
        stability = (self.cycle % 3)
        asc = ["flicker 🌱", "glow 🌿", "bloom 🌳"][stability]

        summary = f"Cycle {self.cycle} | Emerald {emerald}% | Stability {stability} | Ascension {asc}"

        # Store packet for viewer
        self.last_packet = {
            "cycle": self.cycle,
            "sentence": sentence,
            "candidates": candidates,
            "scores": scores,
            "emerald_level": emerald,
            "stability": stability,
            "ascension_state": asc,
            "summary": summary,
        }

        # Emit packet to bus
        self.creature.universal_bus.emit(
            source="brushup",
            channel="brushup",
            kind="refinement",
            payload=self.last_packet,
        )
