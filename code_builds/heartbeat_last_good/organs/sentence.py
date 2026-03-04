# ============================
# sentence_organ.py — Emergent Sentence + I-Organ
# ============================

import random


class SentenceOrgan:
    def __init__(self):
        self.rng = random.Random()

        # -------------------------
        # Template tiers
        # -------------------------
        self.low_templates = [
            "{reaction} lingers near the {world}",
            "soft {reaction} rests by the {world}",
            "the {world} holds a faint {reaction}"
        ]

        self.mid_templates = [
            "{agent} {verb} toward the {world}",
            "in {mood_shade}, {agent} {verb} near the {world}",
            "the {world} stirs as {agent} {verb}"
        ]

        self.high_templates = [
            "{agent} {verb} through the {world}, guided by {idea}",
            "the {world} opens as {agent} {verb} in {mood_shade}",
            "drift carries {agent} toward the {world}"
        ]

        self.mythic_templates = [
            "in {drift_motion}, {agent} becomes {idea} at the {world}",
            "the {world} answers as {agent} {verb} through {idea}",
            "{agent} moves in {drift_motion}, shaping {idea} at the {world}"
        ]

        # -------------------------
        # Vocabulary pools
        # -------------------------
        self.agents = [
            "the pattern", "the echo", "the small self",
            "the watcher", "the inner shape"
        ]

        self.verbs = [
            "moves", "leans", "drifts", "circles", "rests", "wanders"
        ]

        self.reactions = [
            "tension", "warmth", "quiet", "pressure", "softness"
        ]

        self.ideas = [
            "memory", "intention", "shape", "signal", "presence"
        ]

        self.worlds = [
            "quiet valley", "shifting corridor", "bright field",
            "forgotten shrine", "chaotic market"
        ]

    # -------------------------
    # Mood shading
    # -------------------------
    def compute_mood_shade(self, mood):
        if not isinstance(mood, tuple):
            return "a dim mood"

        name, levels = mood
        if not isinstance(levels, dict):
            return name

        calm = levels.get("calm", 0.5)
        alert = levels.get("alert", 0.5)

        if alert > 0.7:
            return "a bright edge"
        if calm > 0.7:
            return "a soft calm"
        return name

    # -------------------------
    # Drift-motion phrasing
    # -------------------------
    def drift_motion_phrase(self, drift):
        if drift["shifted"]:
            return "a rising shift"
        return "a held pattern"

    # -------------------------
    # Template tier selection (Option 2)
    # -------------------------
    def choose_template(self, drift, symbolic_pressure):
        # symbolic pressure boosts drift intensity
        effective_intensity = drift["intensity"] + (symbolic_pressure * 0.5)

        # clamp to [0, 1]
        if effective_intensity < 0.0:
            effective_intensity = 0.0
        if effective_intensity > 1.0:
            effective_intensity = 1.0

        if effective_intensity < 0.25:
            return self.low_templates
        elif effective_intensity < 0.55:
            return self.mid_templates
        elif effective_intensity < 0.85:
            return self.high_templates
        else:
            return self.mythic_templates

    # -------------------------
    # I-Organ resonance
    # -------------------------
    def i_organ_line(self, drift, mood):
        tone = drift["tone"]
        mood_name = mood[0] if isinstance(mood, tuple) else "unknown"

        if drift["shifted"]:
            return f"I feel the shift while {mood_name} moves through me."
        else:
            return f"I remain held as {mood_name} settles."

    # -------------------------
    # Main sentence generator
    # -------------------------
    def generate(self, drift, mood, symbolic_pressure):
        mood_shade = self.compute_mood_shade(mood)
        drift_motion = self.drift_motion_phrase(drift)

        template_pool = self.choose_template(drift, symbolic_pressure)
        template = self.rng.choice(template_pool)

        sentence = template.format(
            agent=self.rng.choice(self.agents),
            verb=self.rng.choice(self.verbs),
            reaction=self.rng.choice(self.reactions),
            idea=self.rng.choice(self.ideas),
            world=self.rng.choice(self.worlds),
            mood_shade=mood_shade,
            drift_motion=drift_motion
        )

        i_line = self.i_organ_line(drift, mood)

        return {
            "sentence": sentence,
            "i_line": i_line
        }
