class ReasonOrgan:
    """
    The Reason Organ classifies sentences into story types
    and provides modifier lists used by the StructureForceEngine.
    """

    def __init__(self):
        # -----------------------------------------------------
        # STORY MODIFIERS (required by StructureForceEngine)
        # -----------------------------------------------------
        self.story_modifiers = {
            "intensifiers": [
                "very", "extremely", "incredibly", "deeply", "wildly",
                "totally", "utterly", "completely", "absolutely"
            ],
            "softeners": [
                "slightly", "somewhat", "barely", "gently", "quietly",
                "almost", "nearly", "kind of", "sort of"
            ],
            "emotion_markers": [
                "sad", "happy", "angry", "afraid", "excited",
                "nervous", "calm", "tense", "hopeful"
            ],
            "structure_markers": [
                "but", "however", "then", "suddenly", "meanwhile",
                "because", "therefore", "after", "before"
            ]
        }

        # -----------------------------------------------------
        # STORY TYPE KEYWORDS
        # -----------------------------------------------------
        self.story_types = {
            "comedy": ["funny", "joke", "laugh", "silly", "gremlin"],
            "horror": ["dark", "fear", "blood", "shadow", "scream"],
            "mythic": ["ancient", "ritual", "spirit", "temple", "myth"],
            "dream": ["float", "drift", "surreal", "fog", "dream"],
            "drama": ["conflict", "emotion", "decision", "tension"]
        }

    # ---------------------------------------------------------
    # CLASSIFIER
    # ---------------------------------------------------------

    def classify_sentence(self, words):
        """
        Very simple keyword-based classifier.
        Later this will evolve into a force-based classifier.
        """

        lower_words = [w.lower() for w in words]

        for story_type, keywords in self.story_types.items():
            for k in keywords:
                if k in lower_words:
                    return story_type

        # fallback
        return "drama"
