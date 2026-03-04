# ------------------------------------------------------------
# SPEECH BLOCK ORGAN
# ------------------------------------------------------------
# This organ generates Speech Blocks: the mathematical,
# semantic, emotional, and social DNA of emergent speech.
#
# It does NOT generate English. That happens in speech_english.py.
# This file only produces the recombinant math substrate.
# ------------------------------------------------------------

from decimal import Decimal
import random
import time

class SpeechBlock:
    def __init__(self, speaker, target, mathblocks, wordforce, speechforce):
        self.id = int(time.time() * 1000)
        self.timestamp = time.time()

        # --------------------------------------------------------
        # MATH CORE — identity substrate
        # --------------------------------------------------------
        primary = random.choice(mathblocks.active_blocks)
        secondary = random.sample(mathblocks.active_blocks, k=min(3, len(mathblocks.active_blocks)))

        self.math_core = {
            "primary_block": primary,
            "secondary_blocks": secondary,
            "drift_vector": [random.random() for _ in range(5)],
            "resonance": mathblocks.compute_resonance(primary, secondary),
            "instability": mathblocks.compute_instability(primary, secondary)
        }

        # --------------------------------------------------------
        # SEMANTIC CORE — meaning substrate
        # --------------------------------------------------------
        concept_seed = wordforce.get_active_concepts(primary)

        self.semantic_core = {
            "concept_seed": concept_seed,
            "word_force_map": wordforce.get_force_map(concept_seed),
            "semantic_drift": random.random(),
            "memory_echo": wordforce.compute_memory_echo(concept_seed)
        }

        # --------------------------------------------------------
        # EMOTIONAL CORE — tone substrate
        # --------------------------------------------------------
        valence, arousal = mathblocks.get_emotional_vector(primary)

        self.emotional_core = {
            "valence": valence,
            "arousal": arousal,
            "pressure": speechforce.pressure,
            "tone": speechforce.get_tone(valence, arousal)
        }

        # --------------------------------------------------------
        # SOCIAL CORE — relational substrate
        # --------------------------------------------------------
        affinity = mathblocks.compute_affinity(speaker, target)
        tension = mathblocks.compute_tension(speaker, target)
        curiosity = mathblocks.compute_curiosity(speaker, target)
        dominance = mathblocks.compute_dominance(speaker, target)
        triad_instability = mathblocks.compute_triad_instability(speaker, target)

        self.social_core = {
            "speaker": speaker,
            "target": target,
            "affinity": affinity,
            "tension": tension,
            "curiosity": curiosity,
            "dominance": dominance,
            "triad_instability": triad_instability
        }

        # --------------------------------------------------------
        # SPEECH FORCE — expression substrate
        # --------------------------------------------------------
        self.speech_force = {
            "pressure": speechforce.pressure,
            "burst": speechforce.burst,
            "inhibition": speechforce.inhibition,
            "urgency": speechforce.urgency
        }

        # --------------------------------------------------------
        # RECOMBINATION — evolution substrate
        # --------------------------------------------------------
        self.recombination = {
            "parent_blocks": [],
            "fusion_pattern": random.choice(["additive", "subtractive", "hybrid", "chaotic"]),
            "mutation_rate": random.random() * 0.2,
            "child_blocks": []
        }

        # --------------------------------------------------------
        # ENGLISH OUTPUT — placeholder only
        # (actual speech is generated in speech_english.py)
        # --------------------------------------------------------
        self.english = {
            "intent": None,
            "template": None,
            "generated_sentence": None
        }

    # ------------------------------------------------------------
    # RECOMBINATION ENGINE
    # ------------------------------------------------------------
    def fuse_with(self, other):
        """Fuse two speech blocks into a new recombinant block."""
        child = SpeechBlock(
            speaker=self.social_core["speaker"],
            target=other.social_core["target"],
            mathblocks=None,      # will be injected by the engine
            wordforce=None,
            speechforce=None
        )

        child.recombination["parent_blocks"] = [self.id, other.id]
        child.recombination["fusion_pattern"] = random.choice(
            ["additive", "subtractive", "hybrid", "chaotic"]
        )

        # Math fusion
        child.math_core["primary_block"] = random.choice([
            self.math_core["primary_block"],
            other.math_core["primary_block"]
        ])

        # Semantic fusion
        child.semantic_core["concept_seed"] = list(
            set(self.semantic_core["concept_seed"] + other.semantic_core["concept_seed"])
        )

        # Emotional fusion
        child.emotional_core["valence"] = (self.emotional_core["valence"] + other.emotional_core["valence"]) / 2
        child.emotional_core["arousal"] = (self.emotional_core["arousal"] + other.emotional_core["arousal"]) / 2

        # Social fusion
        child.social_core["affinity"] = (self.social_core["affinity"] + other.social_core["affinity"]) / 2
        child.social_core["tension"] = (self.social_core["tension"] + other.social_core["tension"]) / 2

        return child
