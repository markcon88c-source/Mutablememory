import random

class HeartOrgan:
    """
    Heart reflects U/W lineage AND begins assigning meaning.
    - Drift intensity controls cluster length
    - Tone controls U/W bias
    - Each cluster gets a word + concept
    - Heart keeps a lexicon (healer list)
    - Now pulls WORDS from ThoughtOrgan
    """

    def __init__(self):
        self.last_cluster = None
        self.lexicon = {}  # cluster → {word, concept}

        # Phase 1: seed vocabulary (fallback)
        self.seed_words = ["soft", "bright", "low", "still", "air", "edge", "field"]
        self.seed_concepts = ["air", "horizon", "breath", "shift", "meaning"]

    def beat(self, tick, drift, thought=None, world=None):
        intensity = drift.get("intensity", 0.0) or 0.0
        tone = drift.get("tone", "rising")

        # Length: 1–8 chars, scaled by drift intensity
        base_len = 1 + int(intensity * 7)

        # Tone bias
        if tone == "rising":
            alphabet = ["U", "U", "W"]
        else:
            alphabet = ["W", "W", "U"]

        cluster = "".join(random.choice(alphabet) for _ in range(base_len))
        self.last_cluster = cluster

        # Create lexicon entry if new
        if cluster not in self.lexicon:
            self.lexicon[cluster] = {
                "word": None,
                "concept": None
            }

        entry = self.lexicon[cluster]

        # ---------------------------------------------------
        # PHASE 2: Thought → word assignment (ACTIVE NOW)
        # ---------------------------------------------------
        if entry["word"] is None and thought is not None:
            phrase = thought.get("phrase")
            if isinstance(phrase, str):
                parts = phrase.split()
                if len(parts) >= 1:
                    entry["word"] = parts[0]  # first word of thought

        # ---------------------------------------------------
        # PHASE 1: Seed fallback (if thought didn't assign)
        # ---------------------------------------------------
        if entry["word"] is None:
            entry["word"] = random.choice(self.seed_words)

        # ---------------------------------------------------
        # PHASE 3 (future): World → concept assignment
        # ---------------------------------------------------
        # if entry["concept"] is None and world is not None:
        #     extracted = self.extract_concept_from_world(world)
        #     if extracted:
        #         entry["concept"] = extracted

        # Seed fallback for concept
        if entry["concept"] is None:
            entry["concept"] = random.choice(self.seed_concepts)

        return {
            "tick": tick,
            "cluster": cluster,
            "intensity": intensity,
            "tone": tone,
            "meaning": entry
        }

    # ---------------------------------------------------
    # Future extraction helpers
    # ---------------------------------------------------
    def extract_concept_from_world(self, world_packet):
        return None
