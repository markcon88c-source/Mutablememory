# organs/example_pool.py
# Provides labeled story-type example sentences.
# SAFE: This organ does nothing unless explicitly called.

class ExamplePool:
    """
    Provides a stable set of example sentences grouped by story type.
    This organ is SAFE and INERT until another organ requests examples.
    """

    def __init__(self):
        self.examples = self._load_examples()

    # ------------------------------------------------------------
    # INTERNAL: Load all 20 story-type fields
    # ------------------------------------------------------------
    def _load_examples(self):
        return {

            "drama": [
                "The argument changed the room in an instant.",
                "She carried the truth like a weight she could not drop.",
                "He stepped forward even though his voice shook.",
                "The choice split the group into uneasy silence.",
                "A secret pressed between them, waiting to break."
            ],

            "tragedy": [
                "He watched the last light fade from the world he knew.",
                "Her hope slipped away before she could reach it.",
                "The fall happened slowly, then all at once.",
                "Loss settled over him like a cold shadow.",
                "The ending arrived long before anyone was ready."
            ],

            "comedy": [
                "He tripped over nothing and apologized to the air.",
                "The plan fell apart before it even began.",
                "She laughed so hard she forgot the problem entirely.",
                "The mistake turned into a joke that lasted all day.",
                "He tried to look serious but failed immediately."
            ],

            "romance": [
                "Their hands brushed, and neither pulled away.",
                "She felt warmth rise when he said her name.",
                "They spoke softly as if the world might overhear.",
                "A quiet promise formed between their smiles.",
                "He waited for her, even when he didn’t have to."
            ],

            "horror": [
                "Something moved in the dark where nothing should be.",
                "The whisper came from behind him, though he was alone.",
                "She felt eyes watching from the corner of the room.",
                "The door creaked open without a single touch.",
                "A cold breath brushed his neck and vanished."
            ],

            "mystery": [
                "A single clue lay hidden in plain sight.",
                "She followed the pattern until it broke unexpectedly.",
                "He sensed a motive buried beneath the silence.",
                "The trail twisted into questions instead of answers.",
                "A shadow moved just before the truth appeared."
            ],

            "adventure": [
                "He stepped onto the path without looking back.",
                "The map led them deeper into unknown land.",
                "She climbed the ridge to see what waited beyond.",
                "The wind carried a promise of danger and discovery.",
                "They pressed forward even when the trail vanished."
            ],

            "epic": [
                "The kingdom held its breath as the storm approached.",
                "He raised the banner and marched into legend.",
                "Her oath echoed across the valley like thunder.",
                "Titans stirred beneath the mountains once more.",
                "A legacy awakened in the heart of a single hero."
            ],

            "mythic": [
                "Fire rose from the stone as the ritual began.",
                "She walked the ancient path carved by forgotten hands.",
                "A spirit answered when he called its true name.",
                "The relic hummed with power older than memory.",
                "Dawn broke with a sign written across the sky."
            ],

            "dream": [
                "She drifted through a world made of soft light.",
                "His footsteps left ripples instead of sound.",
                "The sky folded open like a curtain of mist.",
                "A lantern floated beside her without a flame.",
                "He reached for a door that wasn’t there a moment ago."
            ],

            "surreal": [
                "The walls bent inward as if listening.",
                "Her reflection blinked before she did.",
                "Time folded around him like a loose sheet.",
                "The street melted into a river of color.",
                "He opened a book and found it breathing."
            ],

            "sci_fi": [
                "The signal pulsed with a pattern no one recognized.",
                "She adjusted the circuit until the anomaly stabilized.",
                "The ship drifted past a star that shouldn’t exist.",
                "He scanned the probe and found something watching back.",
                "The orbit shifted without any known force."
            ],

            "fantasy": [
                "She traced the rune and felt it glow beneath her hand.",
                "The blade shimmered with a quiet, ancient power.",
                "A ward flickered as the creature approached.",
                "He followed the grove’s whispering lights.",
                "The sigil opened a path hidden from mortal sight."
            ],

            "chaos": [
                "The ground split before anyone could react.",
                "Colors twisted into shapes that defied reason.",
                "He felt the world tilt sideways for a heartbeat.",
                "The air cracked with sudden, violent energy.",
                "She watched order dissolve into spiraling motion."
            ],

            "slice_of_life": [
                "She sipped her coffee and watched the street wake up.",
                "He folded laundry while humming a quiet tune.",
                "The bus arrived late, but no one seemed to mind.",
                "A warm breeze drifted through the open window.",
                "They shared a quiet moment without needing words."
            ],

            "philosophical": [
                "He questioned the meaning behind every small action.",
                "She wondered whether truth could exist without doubt.",
                "A single idea changed the way he saw the world.",
                "They debated the nature of being until sunrise.",
                "She felt the weight of a paradox settle in her mind."
            ],

            "spiritual": [
                "She breathed deeply and felt the world soften.",
                "A quiet presence rested beside him in the stillness.",
                "Light filtered through the trees like a blessing.",
                "He whispered a prayer without expecting an answer.",
                "Grace found her when she stopped searching."
            ],

            "heroic": [
                "He stepped forward when everyone else stepped back.",
                "She lifted the shield and held the line.",
                "A vow burned in his chest like a living flame.",
                "They stood together against impossible odds.",
                "Courage rose in her like a sudden tide."
            ],

            "melancholic": [
                "He watched the dusk settle over old memories.",
                "She carried an ache she could not name.",
                "The quiet felt heavier than the words they avoided.",
                "He walked alone through a place they once shared.",
                "A soft sadness lingered long after the moment passed."
            ],

            "cosmic": [
                "Stars drifted like slow thoughts across the void.",
                "She felt the horizon stretch beyond understanding.",
                "His pulse matched the rhythm of distant galaxies.",
                "A vast silence wrapped itself around the ship.",
                "The universe opened before them without end."
            ]
        }

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def get_all_types(self):
        """Return a list of all story-type labels."""
        return list(self.examples.keys())

    def get_sentences(self, story_type):
        """Return the list of sentences for a given story type."""
        return self.examples.get(story_type, [])

    def get_random_sentence(self, story_type):
        """Return one random sentence from a story type."""
        import random
        return random.choice(self.examples.get(story_type, []))
