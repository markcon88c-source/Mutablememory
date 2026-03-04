# organs/story_engine_organ.py

from typing import Dict, Any, List


class StoryEngineOrgan:
    """
    The creature's first true narrative engine.
    - Takes the weaver's thread
    - Detects when a beat becomes an event
    - Builds a story spine (list of events)
    - Generates proto-sentences from symbolic beats
    """

    def __init__(self, max_events: int = 50):
        self.spine: List[Dict[str, Any]] = []
        self.max_events = max_events
        self.cycle = 0

    def _beat_to_sentence(self, beat: Dict[str, Any]) -> str:
        """
        Convert a symbolic beat into a proto-sentence.
        This is intentionally simple and mythic.
        """
        word = beat["word"]
        glyph = beat["glyph"]
        stype = beat["story_type"]

        templates = {
            "action": f"The {word} {glyph} surged forward.",
            "dream": f"A vision of {word} {glyph} drifted through the mind.",
            "mythic": f"The ancient {word} {glyph} stirred in the deep.",
            "horror": f"A shadow of {word} {glyph} crept across the edges of thought.",
            "mystery": f"A clue hidden in {word} {glyph} whispered its presence.",
            "drama": f"The memory of {word} {glyph} weighed heavily.",
            "epic": f"The path of {word} {glyph} opened toward destiny.",
        }

        return templates.get(stype, f"The {word} {glyph} moved in silence.")

    def step(self, weaver_state: Dict[str, Any]) -> Dict[str, Any]:
        self.cycle += 1

        thread = weaver_state.get("thread", [])
        if not thread:
            return {
                "cycle": self.cycle,
                "events": list(self.spine),
                "new_event": None,
            }

        # The last beat is the freshest symbolic moment
        beat = thread[-1]

        # Convert beat → event
        sentence = self._beat_to_sentence(beat)

        event = {
            "cycle": self.cycle,
            "word": beat["word"],
            "glyph": beat["glyph"],
            "story_type": beat["story_type"],
            "sentence": sentence,
        }

        # Add to spine
        self.spine.append(event)

        # Trim if needed
        if len(self.spine) > self.max_events:
            self.spine = self.spine[-self.max_events:]

        return {
            "cycle": self.cycle,
            "events": list(self.spine),
            "new_event": event,
        }
