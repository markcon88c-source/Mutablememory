# SENTENCE VIEWER — CATHEDRAL EDITION
# Displays the creature's most recent sentence and related state.

class SentenceViewer:
    def __init__(self, creature):
        self.creature = creature
        self.last_sentence = None

    def update(self, sentence):
        self.last_sentence = sentence

    def tick(self):
        # Pull from creature if available
        if hasattr(self.creature, "last_sentence"):
            self.last_sentence = self.creature.last_sentence
        return self.last_sentence

    def show(self):
        # Human-readable snapshot
        return {
            "sentence": self.last_sentence,
            "state": dict(self.creature.state) if hasattr(self.creature, "state") else {}
        }
