# ============================================================
# RECURSION ORGAN — MULTI‑PASS STABILITY + ASCENSION GATE
# ============================================================

class RecursionOrgan:
    def __init__(self):
        self.current_sentence = ""
        self.pass_number = 0

        # Stability metrics
        self.phonetic_stability = 0.0
        self.force_stability = 0.0
        self.shape_stability = 0.0
        self.grammar_force = 0.0
        self.gravity = 0.0
        self.shape_name = "line"

        # Ascension readiness
        self.ready_for_ascension = False

    # ------------------------------------------------------------
    # Receive a new sentence from SentenceOrgan
    # ------------------------------------------------------------
    def receive(self, packet):
        if packet.get("type") != "sentence":
            return

        payload = packet.get("payload", {})
        self.current_sentence = payload.get("text", "")
        self.pass_number = 0

        # Reset metrics
        self.phonetic_stability = 0.0
        self.force_stability = 0.0
        self.shape_stability = 0.0
        self.grammar_force = 0.0
        self.gravity = payload.get("gravity", 0.0)
        self.shape_name = payload.get("shape", "line")

        self.ready_for_ascension = False

    # ------------------------------------------------------------
    # Compute stability increments per pass
    # ------------------------------------------------------------
    def compute_stability(self):
        # These increments can be tuned later
        self.phonetic_stability = min(1.0, self.phonetic_stability + 0.12)
        self.force_stability = min(1.0, self.force_stability + 0.10)
        self.shape_stability = min(1.0, self.shape_stability + 0.08)
        self.grammar_force = min(1.0, self.grammar_force + 0.06)
        self.gravity = min(1.0, self.gravity + 0.05)

    # ------------------------------------------------------------
    # Compute readiness score
    # ------------------------------------------------------------
    def compute_readiness(self):
        readiness = (
            0.20 * self.phonetic_stability +
            0.20 * self.force_stability +
            0.20 * self.gravity +
            0.20 * self.shape_stability +
            0.20 * self.grammar_force
        )
        return readiness

    # ------------------------------------------------------------
    # Emit a recursion packet
    # ------------------------------------------------------------
    def emit_recursion_packet(self, bus):
        packet = {
            "type": "recursion",
            "payload": {
                "sentence": self.current_sentence,   # 🔥 REQUIRED FOR VIEWER
                "pass": self.pass_number,
                "phonetic_stability": self.phonetic_stability,
                "force_stability": self.force_stability,
                "shape_stability": self.shape_stability,
                "grammar_force": self.grammar_force,
                "gravity": self.gravity,
                "shape": self.shape_name,
                "ready_for_ascension": self.ready_for_ascension,
            }
        }
        bus.send(packet)

    # ------------------------------------------------------------
    # Emit stabilized packet when ready
    # ------------------------------------------------------------
    def emit_stabilized_packet(self, bus):
        packet = {
            "type": "recursion_stabilized",
            "payload": {
                "sentence": self.current_sentence,
                "passes": self.pass_number,
                "gravity": self.gravity,
                "phonetic_stability": self.phonetic_stability,
                "force_stability": self.force_stability,
                "shape_stability": self.shape_stability,
                "grammar_force": self.grammar_force,
                "shape": self.shape_name,
            }
        }
        bus.send(packet)

    # ------------------------------------------------------------
    # Heartbeat tick — run one recursion pass
    # ------------------------------------------------------------
    def tick(self, bus):
        if not self.current_sentence:
            return

        # Update metrics
        self.compute_stability()
        self.pass_number += 1

        # Emit recursion packet
        self.emit_recursion_packet(bus)

        # Check readiness
        readiness = self.compute_readiness()
        if readiness >= 0.85:
            self.ready_for_ascension = True
            self.emit_stabilized_packet(bus)
