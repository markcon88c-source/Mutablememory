# ============================================================
# DIAGNOSTIC SENTENCE EMITTER
# ------------------------------------------------------------
# Forces a simple sentence packet every heartbeat so that
# downstream organs (language, meaning, brushup) always have
# something to process.
# ============================================================

class DiagnosticSentenceEmitter:
    def __init__(self, creature):
        self.creature = creature
        self.counter = 0

    def tick(self):
        self.counter += 1
        sentence = f"diagnostic sentence {self.counter}"

        return {
            "channel": "sentence",
            "kind": "diagnostic",
            "payload": sentence,
        }
