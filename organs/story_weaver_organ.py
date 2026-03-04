# organs/story_weaver_organ.py

from typing import Dict, Any, List


class StoryWeaverOrgan:
    """
    The creature's short-term narrative memory.
    - Collects passing seeds each tick
    - Keeps a rolling thread of recent story beats
    - Tracks motifs and symbolic recurrence
    """

    def __init__(self, max_length: int = 12):
        self.thread: List[Dict[str, Any]] = []
        self.max_length = max_length
        self.cycle = 0

    def step(self, story_seeds: Dict[str, Any]) -> Dict[str, Any]:
        self.cycle += 1

        candidates = story_seeds.get("candidates", [])
        passing = [c for c in candidates if c.get("passes")]

        # Add passing seeds to the thread
        for p in passing:
            self.thread.append({
                "word": p["word"],
                "story_type": p["story_type"],
                "score": p["score"],
                "glyph": p["glyph"],
                "cycle": self.cycle,
            })

        # Trim to max length
        if len(self.thread) > self.max_length:
            self.thread = self.thread[-self.max_length:]

        # Compute motif frequencies
        motifs = {}
        for beat in self.thread:
            w = beat["word"]
            motifs[w] = motifs.get(w, 0) + 1

        return {
            "cycle": self.cycle,
            "thread": list(self.thread),
            "motifs": motifs,
            "passing_count": len(passing),
        }
