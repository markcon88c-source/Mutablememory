# organs/story_seed_organ.py

from typing import Dict, Any, List
import random


class StorySeedOrgan:
    """
    Evaluates candidate words + MathBlock forces and decides:
    - story type
    - entry score
    - pass/fail
    - reasons
    This is the first step of the story game.
    """

    def __init__(self):
        self.cycle = 0

    def _story_type_from_forces(self, forces: Dict[str, float], glyph: str, heart: Dict[str, Any]) -> str:
        spark = forces.get("spark", 0.0)
        drift = forces.get("drift", 0.0)
        echo = forces.get("echo", 0.0)
        chaos = forces.get("chaos", 0.0)
        clarity = forces.get("clarity", 0.0)
        memory = forces.get("memory", 0.0)
        pressure = forces.get("pressure", 0.0)

        # base type from dominant force
        force_map = {
            "spark": ("action", spark),
            "drift": ("dream", drift),
            "echo": ("mythic", echo),
            "chaos": ("horror", chaos),
            "clarity": ("mystery", clarity),
            "memory": ("drama", memory),
            "pressure": ("epic", pressure),
        }
        base_type, _ = max(force_map.values(), key=lambda x: x[1])

        polarity = heart.get("polarity", 0.0)
        resonance = heart.get("resonance", 0.0)

        # glyph tilt
        if "🔥" in glyph or "⚔" in glyph:
            base_type = "action"
        elif "🌫" in glyph or "🌙" in glyph:
            base_type = "dream"
        elif "🌀" in glyph or "⛓" in glyph:
            base_type = "mythic"

        # heart tilt
        if resonance > 0.7 and base_type in ["drama", "mythic"]:
            base_type = "mythic"
        if polarity < -0.6 and chaos > 0.4:
            base_type = "horror"

        return base_type

    def _reasons_for_failure(self, forces: Dict[str, float], heart: Dict[str, Any]) -> List[str]:
        reasons = []
        chaos = forces.get("chaos", 0.0)
        clarity = forces.get("clarity", 0.0)
        memory = forces.get("memory", 0.0)
        pressure = forces.get("pressure", 0.0)
        drift = forces.get("drift", 0.0)

        polarity = heart.get("polarity", 0.0)
        resonance = heart.get("resonance", 0.0)

        if chaos > 0.7:
            reasons.append("chaos spike too high")
        if clarity < 0.2:
            reasons.append("not clear enough to place in story")
        if memory < 0.2 and resonance > 0.5:
            reasons.append("heart wants something more meaningful")
        if pressure < 0.1:
            reasons.append("no narrative pressure yet")
        if drift > 0.8:
            reasons.append("drifting too far from current focus")
        if polarity < -0.6:
            reasons.append("heart polarity too negative for this word")

        return reasons

    def evaluate_candidate(
        self,
        word: str,
        forces: Dict[str, float],
        glyph: str,
        heart: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate a single word + forces.
        Returns a viewer-ready dict with reasons.
        """
        story_type = self._story_type_from_forces(forces, glyph, heart)

        score = (
            forces.get("spark", 0.0) * 0.2 +
            forces.get("echo", 0.0) * 0.2 +
            forces.get("memory", 0.0) * 0.2 +
            forces.get("pressure", 0.0) * 0.2 +
            forces.get("clarity", 0.0) * 0.2
        )

        reasons_fail = self._reasons_for_failure(forces, heart)
        passes = score > 0.4 and not reasons_fail

        return {
            "word": word,
            "story_type": story_type,
            "score": round(score, 3),
            "passes": passes,
            "reasons_fail": reasons_fail,
            "forces": forces,
            "glyph": glyph,
        }

    def step(self, mathblocks_state: Dict[str, Any], heart: Dict[str, Any]) -> Dict[str, Any]:
        """
        Take current MathBlock state and heart, evaluate a few candidates.
        Expects mathblocks_state to have:
        {
          "blocks": [
             {"word": "...", "forces": {...}, "glyph": "..."},
             ...
          ]
        }
        """
        self.cycle += 1
        blocks = mathblocks_state.get("blocks", [])
        if not blocks:
            return {"cycle": self.cycle, "candidates": []}

        sample = random.sample(blocks, k=min(5, len(blocks)))

        evaluated = [
            self.evaluate_candidate(
                b.get("word", "?"),
                b.get("forces", {}),
                b.get("glyph", ""),
                heart,
            )
            for b in sample
        ]

        return {
            "cycle": self.cycle,
            "candidates": evaluated,
        }
