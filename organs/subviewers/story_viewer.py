import random
import time

from organs.punctuation_pressure import PunctuationPressure


# ---------------------------------------------------------
# Force → Color Map (full force stack)
# ---------------------------------------------------------
FORCE_COLORS = {
    "mood": "🟪",        # emotional tone
    "stm": "🟦",         # memory flow
    "story": "🟧",       # narrative tension
    "idea": "🟨",        # conceptual energy
    "mathblock": "🟥",   # structural force
    "sentence": "🟩",    # local sentence pressure
    "world": "⬜",       # worldbuilding gravity
    "word": "⬛",        # word-level microforce
}

MOOD_EMOJIS = {
    "calm": "🌿",
    "alert": "⚡",
    "curious": "🔍",
    "bright": "✨",
}

IDEA_EMOJI = "💡"
STORY_EMOJI = "📖"
DOT_EMOJI = "•"


class StoryViewer:
    def __init__(self, creature):
        self.creature = creature
        self.line_delay = 0.10
        self.punct = PunctuationPressure(creature)

    def crawl(self, text=""):
        print(text)
        time.sleep(self.line_delay)

    # ---------------------------------------------------------
    # Force Vector (samples all major pressures)
    # ---------------------------------------------------------
    def get_force_vector(self):
        mood_state = self.creature.mood.state
        mood = max(mood_state.values())

        stm = len(self.creature.stm.active_words) / 10

        story = getattr(self.creature.world, "tension", 0.0)

        # Idea pressure = average idea strength
        idea_total = 0.0
        ideas = getattr(self.creature.world, "ideas", [])
        for idea_obj in ideas:
            idea_total += idea_obj.forces.get("strength", 0.0)
        idea = idea_total / max(1, len(ideas))

        mathblock = getattr(self.creature.mathblocks, "global_pressure", 0.0)

        sentence = (
            self.creature.pressure_core.focus +
            self.creature.pressure_core.drift +
            self.creature.pressure_core.pause
        )

        world = getattr(self.creature.world, "gravity", 0.0)

        word = getattr(self.creature.word_pressure, "total_pressure", 0.0)

        return {
            "mood": mood,
            "stm": stm,
            "story": story,
            "idea": idea,
            "mathblock": mathblock,
            "sentence": sentence,
            "world": world,
            "word": word,
        }

    # ---------------------------------------------------------
    # Dominant Force (winner of the force stack)
    # ---------------------------------------------------------
    def get_dominant_force(self):
        forces = self.get_force_vector()
        return max(forces, key=forces.get)

    # ---------------------------------------------------------
    # Choose ideas based on idea forces
    # ---------------------------------------------------------
    def choose_ideas(self):
        ideas = getattr(self.creature.world, "ideas", [])
        if not ideas:
            return []

        weighted = []
        for idea in ideas:
            forces = getattr(idea, "forces", {})
            strength = float(forces.get("strength", 0.0))
            resonance = float(forces.get("resonance", 0.0))
            clustering = float(forces.get("clustering", 0.0))
            weight = strength + resonance + clustering
            weighted.append((idea, weight))

        total = sum(w for _, w in weighted) or 1.0
        normalized = [(i, w / total) for i, w in weighted]

        choices = [i for i, _ in normalized]
        weights = [w for _, w in normalized]

        k = random.randint(2, 4)
        chosen = random.choices(choices, weights=weights, k=k)
        return chosen

    # ---------------------------------------------------------
    # Build a story-like sentence with punctuation + force color
    # ---------------------------------------------------------
    def build_sentence(self, ideas):
        if not ideas:
            return "The world is quiet. 🌙"

        words = []
        for idea in ideas:
            idea_words = getattr(idea, "words", None)
            if idea_words:
                words.extend(idea_words)
            else:
                words.append("something")

        random.shuffle(words)
        words = words[:random.randint(6, 14)]

        if words:
            words[0] = words[0].capitalize()

        # Update punctuation pressure
        self.punct.update()

        # Mid-sentence punctuation experiments
        for i in range(1, len(words) - 1):
            if random.random() < 0.15:
                p = self.punct.choose()

                if p in [",", "—", "…"]:
                    words[i] = words[i] + p
                elif p == "\n":
                    words[i] = words[i] + "\n"
                elif p == "    ":
                    words[i] = words[i] + "\n    "

        # End punctuation
        end_punct = self.punct.choose()
        if end_punct in ["\n", "    "]:
            end_punct = "."

        # Mood emoji
        mood_state = self.creature.mood.state
        mood_key = max(mood_state, key=mood_state.get)
        mood_emoji = MOOD_EMOJIS.get(mood_key, "✨")

        # Force color signature
        dominant = self.get_dominant_force()
        color = FORCE_COLORS.get(dominant, "⬜")

        sentence = " ".join(words) + end_punct + " " + color + " " + mood_emoji
        return sentence

    # ---------------------------------------------------------
    # Show the story viewer output
    # ---------------------------------------------------------
    def show(self):
        self.crawl("")
        self.crawl(f"{STORY_EMOJI} STORY VIEWER")
        self.crawl("────────────────────────────")

        ideas = self.choose_ideas()
        sentence = self.build_sentence(ideas)

        self.crawl("Story Sentence:")
        self.crawl(f"  \"{sentence}\"")
        self.crawl("")

        self.crawl("Ideas used:")
        if not ideas:
            self.crawl(f"  {DOT_EMOJI} (none)")
        else:
            for idea in ideas:
                label = getattr(idea, "label", None)
                if label:
                    self.crawl(f"  {IDEA_EMOJI} {label}")
                else:
                    self.crawl(f"  {IDEA_EMOJI} {idea}")
        self.crawl("")
