# EnglishReservoir.py

class EnglishReservoir:
    def __init__(self, story_types, scorer):
        self.story_types = story_types
        self.scorer = scorer

    def score(self, sentence_text, bucket):
        try:
            return self.scorer(sentence_text, bucket)
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
