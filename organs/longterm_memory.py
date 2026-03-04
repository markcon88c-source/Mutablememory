import json
import os

class LongTermMemoryOrgan:
    """
    Long-term memory organ.
    Stores only meaningful events based on:
      - memory_score
      - mood_name
      - drift_shifted
      - emphasis
      - character_presence
      - selector_choice
    """

    def __init__(self, path="longterm_memory.json"):
        self.path = path
        self.data = {
            "core_memories": [],
            "high_scores": [],
            "low_scores": [],
            "character_events": [],
            "mood_events": [],
            "selector_events": []
        }
        self.load()

    def load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except Exception:
            pass

    def save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def should_store(self, memory_score, emphasis):
        """
        Decide if this moment deserves long-term storage.
        """
        if memory_score > 0.85:
            return True
        if memory_score < 0.15:
            return True
        if emphasis:
            return True
        return False

    def store_event(self, packet):
        """
        Store a packet into the correct category.
        packet contains:
          - english_final
          - memory_score
          - mood_name
          - drift_shifted
          - emphasis
          - character_presence
          - selector_choice
        """

        score = packet.get("memory_score", 0.0)
        mood = packet.get("mood_name", "unknown")
        drift = packet.get("drift_shifted", False)
        emph = packet.get("emphasis", False)
        charp = packet.get("character_presence", 0.0)
        sel = packet.get("selector_choice", "none")
        text = packet.get("english_final", "")

        event = {
            "text": text,
            "score": score,
            "mood": mood,
            "drift": drift,
            "emphasis": emph,
            "character_presence": charp,
            "selector": sel
        }

        if score > 0.85:
            self.data["high_scores"].append(event)
        elif score < 0.15:
            self.data["low_scores"].append(event)

        if charp > 0.6:
            self.data["character_events"].append(event)

        if emph:
            self.data["core_memories"].append(event)

        self.data["mood_events"].append({
            "mood": mood,
            "text": text
        })

        self.data["selector_events"].append({
            "selector": sel,
            "text": text
        })

        self.save()

    def process(self, packet):
        """
        Main entry point.
        packet must contain:
          - english_final
          - memory_score
          - mood_name
          - drift_shifted
          - emphasis
          - character_presence
          - selector_choice
        Returns:
          - stored (bool)
          - reason (str)
        """

        score = packet.get("memory_score", 0.0)
        emph = packet.get("emphasis", False)

        if not self.should_store(score, emph):
            return False, "Not meaningful enough for long-term memory"

        self.store_event(packet)
        return True, "Stored in long-term memory"
