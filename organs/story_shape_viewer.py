# organs/story_shape_viewer.py
# Reservoir words drifting into story-shape clusters

class StoryShapeViewer:
    def __init__(self, creature):
        self.creature = creature
        self.last_shapes = {}

        # Default story clusters (you can expand these)
        self.story_clusters = {
            "romance": ["soft", "warm", "touch", "longing"],
            "horror": ["dark", "cold", "whisper", "shadow"],
            "epic": ["storm", "oath", "banner", "stride"],
            "dream": ["float", "echo", "glow", "veil"],
            "drama": ["ache", "break", "hold", "truth"],
        }

    def compute_shape_match(self, word):
        """
        Compute which story cluster the word drifts toward.
        Very simple similarity for now: shared letters or vibe tags.
        """
        word_lower = word.lower()
        scores = {}

        for cluster, anchors in self.story_clusters.items():
            score = 0
            for anchor in anchors:
                # crude similarity: shared characters
                shared = len(set(word_lower) & set(anchor))
                score += shared
            scores[cluster] = score

        # pick best cluster
        best_cluster = max(scores, key=scores.get)
        best_score = scores[best_cluster]

        # if score is zero, it "bounces"
        if best_score == 0:
            return {"cluster": None, "score": 0, "status": "bounce"}

        return {"cluster": best_cluster, "score": best_score, "status": "bond"}

    def receive(self, packets):
        """
        Extract reservoir words from packets and compute their story-shape drift.
        """
        shapes = {}

        for p in packets:
            if p.get("type") == "reservoir_word":
                word = p.get("word")
                if not word:
                    continue

                result = self.compute_shape_match(word)
                shapes[word] = result

        self.last_shapes = shapes

    def display(self):
        print("\n=== STORY SHAPE VIEWER ===")

        if not self.last_shapes:
            print("(no reservoir words processed yet)")
            return

        for word, info in self.last_shapes.items():
            status = info["status"]
            cluster = info["cluster"]
            score = info["score"]

            if status == "bounce":
                print(f"{word:15} → bounced off all story shapes")
            else:
                print(f"{word:15} → drifted to {cluster} (score {score})")
