# organofsentence.py
# ============================================================
# OrganOfSentence — stores preview + final sentences
# ============================================================

class OrganOfSentence:
    def __init__(self):
        self.preview_sentence = ""
        self.final_sentence = ""

    # Called every breath by IterationViewer PRIME
    def update_sentences(self, preview_sentence="", final_sentence=""):
        if preview_sentence:
            self.preview_sentence = preview_sentence
        if final_sentence:
            self.final_sentence = final_sentence

    # Language Viewer pulls this
    def get_next_sentence(self):
        return self.preview_sentence

    # Heartbeat pulls this
    def get_last_sentence(self):
        return self.final_sentence
