# story_gravity_reservoir_loader.py

class EnglishReservoir:
    def __init__(self):
        # Built-in default story types
        self.story_types = [
            "mythic",
            "cosmic",
            "slice",
            "technical",
        ]

        # Default scorer: neutral, can be replaced later
        self.scorer = self._default_scorer

        # Optional: bucket word lists (empty for now)
        self.bucket_words = {
            "mythic": [],
            "cosmic": [],
            "slice": [],
            "technical": [],
        }

    def _default_scorer(self, sentence_text, bucket):
        return 0.0

    def score(self, sentence_text, bucket):
        try:
            val = self.scorer(sentence_text, bucket)
            if isinstance(val, (int, float)):
                return float(val)
            return 0.0
        except Exception:
            return 0.0

    def leaning(self, sentence_text):
        scores = {}
        for bucket in self.story_types:
            s = self.score(sentence_text, bucket)
            scores[bucket] = s
        return scores

    def best_bucket(self, sentence_text):
        scores = self.leaning(sentence_text)
        if not scores:
            return None
        return max(scores, key=scores.get)

    def bucket(self, bucket_type):
        # Return the words for this bucket
        return self.bucket_words.get(bucket_type, [])
