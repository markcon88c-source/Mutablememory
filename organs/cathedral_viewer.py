# CATHEDRAL VIEWER — METABOLIC PANEL

class CathedralViewer:
    def __init__(self, creature=None):
        self.creature = creature
        self.last_sentence = None
        self.last_language_stats = {}
        self.last_narrative_metrics = {}
        self.last_brushup = None
        self.last_emergence = None

    def _get_sentence(self, creature):
        sv = getattr(creature, "sentence_viewer", None)
        if sv and hasattr(sv, "last_sentence"):
            return sv.last_sentence
        return getattr(creature, "last_sentence", None)

    def _get_language_stats(self, creature):
        vocab = getattr(creature, "vocabulary", None)
        stats = {}
        if vocab is not None:
            size = len(getattr(vocab, "lexicon", {})) if hasattr(vocab, "lexicon") else None
            stats["vocab_size"] = size
        return stats

    def _get_narrative_metrics(self, creature):
        sm = getattr(creature, "story_metrics", None)
        if sm is not None and hasattr(sm, "metrics"):
            return sm.metrics
        return {}

    def _get_brushup(self, creature):
        # Placeholder hook for your brush-up system
        bu = getattr(creature, "brushup", None)
        if bu is not None and hasattr(bu, "last_result"):
            return bu.last_result
        return None

    def _get_emergence(self, creature):
        eg = getattr(creature, "emergence_gate", None)
        if eg is not None and hasattr(eg, "last_status"):
            return eg.last_status
        return None

    def update(self, creature):
        self.creature = creature

        self.last_sentence = self._get_sentence(creature)
        self.last_language_stats = self._get_language_stats(creature)
        self.last_narrative_metrics = self._get_narrative_metrics(creature)
        self.last_brushup = self._get_brushup(creature)
        self.last_emergence = self._get_emergence(creature)

        hb = getattr(creature, "heartbeat_count", 0)

        print("────────────────────────────────────────────")
        print(f"Heartbeat: {hb}")
        print("────────────────────────────────────────────")

        # Sentence metabolism
        print("Sentence Metabolism:")
        print(f"  Sentence: {self.last_sentence!r}")
        print()

        # Language
        print("Language:")
        vs = self.last_language_stats.get("vocab_size")
        print(f"  Vocab size: {vs}")
        print()

        # Narrative
        print("Narrative Metrics:")
        for k, v in self.last_narrative_metrics.items():
            print(f"  {k}: {v}")
        print()

        # Brush-up
        print("Brush-Up:")
        print(f"  Last: {self.last_brushup}")
        print()

        # Emergence
        print("Emergence:")
        print(f"  Status: {self.last_emergence}")
        print()
