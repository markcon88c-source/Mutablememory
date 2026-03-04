class SentenceAttemptTube:
    """
    Stores all sentence attempts so the creature can revisit them later.
    """

    def __init__(self):
        self.attempts = []

    def add_attempt(self, words, forces, stability, state, story_type=None):
        self.attempts.append({
            "words": words[:],
            "forces": forces.copy(),
            "stability": stability,
            "state": state,
            "story_type": story_type
        })

    def get_random_attempt(self):
        if not self.attempts:
            return None
        import random
        return random.choice(self.attempts)

    def get_unformed(self):
        return [a for a in self.attempts if a["state"] == "UNFORMED"]

    def get_recent(self, n=5):
        return self.attempts[-n:]
