class EnglishOrgan:
    def __init__(self):
        pass

    def generate_sentence(self, verb=None, reaction=None, world=None, mood=None):
        # If anything is missing, return none
        if verb is None or reaction is None or world is None or mood is None:
            return "none"

        # Mood may be a tuple like ('calm', {...})
        if isinstance(mood, tuple):
            mood_word = mood[0]
        else:
            mood_word = str(mood)

        # Reaction may be None or a string
        reaction_word = reaction if reaction else "responds"

        # Build the sentence
        sentence = f"{verb.capitalize()} {reaction_word} in {world} while feeling {mood_word}."
        return sentence
class EnglishOrgan:
    def __init__(self):
        pass

    def generate_sentence(self, verb=None, reaction=None, world=None, mood=None):
        if verb is None or world is None or mood is None:
            return "none"

        if isinstance(mood, tuple):
            mood_word = mood[0]
        else:
            mood_word = str(mood)

        if not reaction:
            reaction = "responds"

        return f"{verb.capitalize()} {reaction} in {world} while feeling {mood_word}."
