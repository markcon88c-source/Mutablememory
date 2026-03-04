# sentence_buffer.py
# Keeps a sentence visible for multiple ticks with slight randomness.
# Viewer-only. Does NOT affect pressures, organs, STM, or math.

import random

BASE_TTL = 3        # average number of ticks to hold a sentence
RANDOM_DRIFT = 1    # +/- drift

class SentenceBuffer:
    def __init__(self, base_ttl=BASE_TTL, drift=RANDOM_DRIFT):
        self.base_ttl = base_ttl
        self.drift = drift
        self.ttl = 0
        self.current_sentence = ""

    def _new_ttl(self):
        """
        Returns a randomized TTL based on base_ttl +/- drift.
        """
        return max(1, self.base_ttl + random.randint(-self.drift, self.drift))

    def update(self, new_sentence):
        """
        Called every tick with the freshly generated sentence.
        Only replaces the displayed sentence when TTL expires.
        """
        if self.ttl <= 0:
            # Accept the new sentence and assign a randomized TTL
            self.current_sentence = new_sentence
            self.ttl = self._new_ttl()
        else:
            # Keep the old sentence
            self.ttl -= 1

        return self.current_sentence
