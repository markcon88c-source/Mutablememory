class MoodOrgan:
    """
    Computes the creature's emotional state from text input:
    - valence (positive/negative)
    - arousal (energy)
    - stability (groundedness)

    All values move incrementally toward targets.
    """

    def __init__(self):
        self.valence = 0.5
        self.arousal = 0.5
        self.stability = 0.5

    def compute(self, text):
        # -----------------------------------------
        # 1. Basic text features
        # -----------------------------------------
        length = len(text)
        has_exclaim = "!" in text
        has_question = "?" in text
        upper_ratio = sum(1 for c in text if c.isupper()) / max(1, len(text))

        # -----------------------------------------
        # 2. Target valence
        # -----------------------------------------
        valence_target = 0.5
        if any(w in text.lower() for w in ["good", "love", "yes", "ok", "cool"]):
            valence_target += 0.2
        if any(w in text.lower() for w in ["bad", "no", "hate", "angry", "sad"]):
            valence_target -= 0.2

        valence_target = max(0.0, min(1.0, valence_target))

        # -----------------------------------------
        # 3. Target arousal
        # -----------------------------------------
        arousal_target = 0.3 + min(0.7, length / 50)
        if has_exclaim:
            arousal_target += 0.2
        if upper_ratio > 0.2:
            arousal_target += 0.1

        arousal_target = max(0.0, min(1.0, arousal_target))

        # -----------------------------------------
        # 4. Target stability
        # -----------------------------------------
        stability_target = 0.6
        if has_question:
            stability_target -= 0.1
        if has_exclaim:
            stability_target -= 0.1

        stability_target = max(0.0, min(1.0, stability_target))

        # -----------------------------------------
        # 5. Incremental movement
        # -----------------------------------------
        def step(current, target, rate=0.15):
            return current + (target - current) * rate

        self.valence = step(self.valence, valence_target)
        self.arousal = step(self.arousal, arousal_target)
        self.stability = step(self.stability, stability_target)

        return {
            "valence": round(self.valence, 2),
            "arousal": round(self.arousal, 2),
            "stability": round(self.stability, 2),
        }


