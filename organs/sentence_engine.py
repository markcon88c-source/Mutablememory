# ============================================================
# SENTENCE ENGINE — TOKEN → SENTENCE ASSEMBLY LOGIC
# ------------------------------------------------------------
# This organ provides a simple, stable interface for turning
# tokens into sentences. SentenceBuilderOrgan uses this engine
# to decide when a sentence is complete.
# ============================================================

class SentenceEngine:
    def __init__(self, creature):
        self.creature = creature
        self.buffer = []
        self.last_sentence = ""
        self.min_length = 3  # minimum tokens before emitting

    # --------------------------------------------------------
    # ADD TOKEN
    # --------------------------------------------------------
    def add_token(self, token):
        if not token:
            return

        self.buffer.append(token)

        # If buffer is long enough, emit a sentence
        if len(self.buffer) >= self.min_length:
            sentence = " ".join(self.buffer)
            self.last_sentence = sentence
            self.buffer = []  # reset buffer
            return sentence

        return None

    # --------------------------------------------------------
    # FORCE EMIT (used by SentenceBuilder if needed)
    # --------------------------------------------------------
    def force_emit(self):
        if not self.buffer:
            return None

        sentence = " ".join(self.buffer)
        self.last_sentence = sentence
        self.buffer = []
        return sentence
