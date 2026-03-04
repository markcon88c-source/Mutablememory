# Cathedral Creature — upgraded for threaded ExecutiveOrgan
# Full metabolic chain including:
# Vocabulary → Lexical → Meaning → ProtoSentence → Sentence → Recursion → Language → Viewers

import time

# BUS
from organs.universal_bus_organ import UniversalBusOrgan

# EXECUTIVE ORGAN (threaded heartbeat + compositor)
from organs.executive_organ import ExecutiveOrgan

# ORGANS
from organs.meaning_organ import MeaningOrgan
from organs.sentence_organ import SentenceOrgan
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.language_organ import LanguageOrgan
from organs.drift_organ import DriftOrgan
from organs.stm_organ import STMOrgan
from organs.story_organ import StoryOrgan
from organs.ocean_organ import OceanOrgan
from organs.pressure_organ import PressureOrgan
from organs.identity_organ import IdentityOrgan
from organs.shore_organ import ShoreOrgan

# VOCABULARY + LEXICAL LAYER
from organs.vocabulary_organ import VocabularyOrgan
from organs.lexical_organ import LexicalOrgan

# PROTO SENTENCE ORGAN
from organs.proto_sentence_organ import ProtoSentenceOrgan

# MATHBLOCKS ORGAN (added)
from organs.mathblocks import MathBlocks

# RECURSION ORGAN
from organs.recursion_organ import RecursionOrgan

# VIEWERS
from viewers.meaning_viewer import MeaningViewer
from viewers.sentence_viewer import SentenceViewer
from viewers.language_viewer import LanguageViewer
from viewers.drift_viewer import DriftViewer
from viewers.story_viewer import StoryViewer
from viewers.ocean_viewer import OceanViewer
from viewers.diagnostic_viewer import DiagnosticViewer
from viewers.heartbeat_viewer import HeartbeatViewer
from viewers.stm_gravity_viewer import STMGravityViewer
from viewers.stm_integrity_viewer import STMIntegrityViewer


class CathedralCreature:
    def __init__(self):

        # Shared bus for all organs + viewers
        self.bus = UniversalBusOrgan()

        # Heartbeat counter + last packet
        self.heartbeat_counter = 0
        self.last_packet = None

        # ----------------------------------------------------
        # VOCABULARY + LEXICAL LAYER
        # ----------------------------------------------------
        self.vocabulary = VocabularyOrgan(self)
        self.lexical = LexicalOrgan(self, self.vocabulary)

        # ----------------------------------------------------
        # MATHBLOCKS ORGAN (must exist BEFORE recursion)
        # ----------------------------------------------------
        self.mathblocks = MathBlocks(self)

        # ----------------------------------------------------
        # EXECUTIVE ORGAN (threaded heartbeat + compositor)
        # ----------------------------------------------------
        self.executive = ExecutiveOrgan(self, heartbeat_interval=0.25)

        # ----------------------------------------------------
        # CORE ORGANS — LIST FORM REQUIRED BY EXECUTIVE ORGAN
        # ----------------------------------------------------
        self.organs = [
            # Executive Organ FIRST (but NOT ticked by creature)
            self.executive,

            # Upstream metabolic signals
            PressureOrgan(self),
            IdentityOrgan(self),
            DriftOrgan(self),
            OceanOrgan(self),
            STMOrgan(self),

            # StoryOrgan
            StoryOrgan(self),

            # Vocabulary + Lexical (nutrient layer)
            self.vocabulary,
            self.lexical,

            # MathBlocks (identity signature layer)
            self.mathblocks,

            # Meaning → ProtoSentence → Sentence
            MeaningOrgan(self),
            ProtoSentenceOrgan(self),
            SentenceOrgan(self),

            # Recursion Organ (stabilizes sentence before ascension)
            RecursionOrgan(self),

            # SentenceBuilder + Language (ascension pathway)
            SentenceBuilderOrgan(self),
            LanguageOrgan(self),

            # Membrane organ last
            ShoreOrgan(self),
        ]

        # Add silent tick to ShoreOrgan to prevent errors if needed
        shore = self.organs[-1]
        if not hasattr(shore, "tick"):
            setattr(shore, "tick", lambda self=None: None)

        # Compatibility alias
        self.organs_list = self.organs

        # ----------------------------------------------------
        # VIEWERS
        # ----------------------------------------------------

        # Named SentenceViewer required by ExecutiveOrgan
        self.sentence_viewer = SentenceViewer()

        self.viewers = [
            MeaningViewer(),
            self.sentence_viewer,   # ExecutiveOrgan depends on this
            LanguageViewer(),
            DriftViewer(),
            StoryViewer(),
            OceanViewer(),
            DiagnosticViewer(),
            HeartbeatViewer(),
            STMGravityViewer(),
            STMIntegrityViewer(),
        ]

        # ----------------------------------------------------
        # REGISTER ORGANS
        # ----------------------------------------------------
        for organ in self.organs:
            self.bus.register(organ)

        # ----------------------------------------------------
        # REGISTER VIEWERS
        # ----------------------------------------------------
        for viewer in self.viewers:
            self.bus.register(viewer)

        # ----------------------------------------------------
        # METABOLIC SPARK — harmless seed
        # ----------------------------------------------------
        self.bus.emit({
            "type": "vocabulary_seed",
            "payload": {
                "tokens": ["the", "creature", "awakens"]
            }
        })

        # ----------------------------------------------------
        # START EXECUTIVE ORGAN THREAD
        # ----------------------------------------------------
        self.executive.start()

    # --------------------------------------------------------
    # TICK ALL ORGANS — CALLED BY EXECUTIVE ORGAN ONLY
    # --------------------------------------------------------
    def tick_all(self):
        # Tick vocabulary + lexical first
        if hasattr(self.vocabulary, "tick"):
            self.vocabulary.tick()
        if hasattr(self.lexical, "tick"):
            self.lexical.tick()

        # Tick all other organs EXCEPT ExecutiveOrgan
        for organ in self.organs:
            if organ is self.executive:
                continue
            tick_fn = getattr(organ, "tick", None)
            if callable(tick_fn):
                tick_fn()

    # --------------------------------------------------------
    # LEGACY TICK (NO LONGER USED)
    # --------------------------------------------------------
    def tick(self):
        pass


if __name__ == "__main__":
    creature = CathedralCreature()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCathedral Creature shutting down.")
