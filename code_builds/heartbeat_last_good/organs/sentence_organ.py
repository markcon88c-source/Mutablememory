import random

class SentenceOrgan:
    def __init__(self):
        self.rng = random.Random()

    def _strongest_memory(self, memory):
        if not memory:
            return None
        return max(memory, key=lambda m: float(m.get("meaning", 0.0)))

    def step(self, thought, world, heart, memory):
        t_words = thought.get("words", [])
        place = world.get("place", "")
        h_word = heart.get("word", "")
        h_concept = heart.get("concept", "")
        cluster = heart.get("cluster", "")

        strongest = self._strongest_memory(memory)
        if strongest:
            mem_word = strongest.get("word", "")
        else:
            mem_word = ""

        parts = []

        if place:
            parts.append("In the " + place + ",")

        if h_word:
            parts.append("my heart speaks " + h_word)

        if h_concept:
            parts.append("of " + h_concept)

        if mem_word:
            parts.append("remembering " + mem_word)

        if t_words:
            parts.append("as I sense " + self.rng.choice(t_words))

        if cluster:
            parts.append("(" + cluster + ")")

        sentence = " ".join(parts)
        return sentence.strip()
