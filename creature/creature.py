# creature/creature.py

from organs.vocabulary_organ import VocabularyOrgan
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.sentence_organ import SentenceOrgan
from organs.language_organ import LanguageOrgan
from organs.packet_bus_organ import PacketBusOrgan
from organs.stm_organ import STMOrgan


class Creature:
    """
    Cathedral creature core.
    Runs organs in metabolic order and hands packets to viewers.
    """

    def __init__(self, viewers=None):
        # Heartbeat counter (used by VocabularyOrgan.tick)
        self.heartbeat_counter = 0

        # ----------------------------------------------------
        # ORGAN REGISTRY (placeholder keys so organs can read it)
        # ----------------------------------------------------
        self.organs = {
            "vocabulary": None,
            "builder": None,
            "sentence": None,
            "language": None,
            "bus": None,
            "stm": None,
        }

        # ----------------------------------------------------
        # VIEWER REGISTRY
        # ----------------------------------------------------
        self.viewer_registry = {}

        # ----------------------------------------------------
        # INSTANTIATE ORGANS
        # ----------------------------------------------------
        self.vocabulary = VocabularyOrgan(self)
        self.builder = SentenceBuilderOrgan(self)
        self.sentence = SentenceOrgan(self)
        self.language = LanguageOrgan(self)
        self.bus = PacketBusOrgan(self)
        self.stm = STMOrgan(self)

        # ----------------------------------------------------
        # POPULATE ORGAN REGISTRY
        # ----------------------------------------------------
        self.organs["vocabulary"] = self.vocabulary
        self.organs["builder"] = self.builder
        self.organs["sentence"] = self.sentence
        self.organs["language"] = self.language
        self.organs["bus"] = self.bus
        self.organs["stm"] = self.stm

        # ----------------------------------------------------
        # METABOLIC PIPELINE
        # ----------------------------------------------------
        self.pipeline = [
            self.vocabulary.step,
            self.builder.step,
            self.sentence.step,
            self.language.step,
            self.bus.step,
            self.stm.step,
        ]

    # --------------------------------------------------------
    # ORGAN REGISTRATION (used by main_organs.py)
    # --------------------------------------------------------
    def register(self, name, organ):
        self.organs[name] = organ
        return organ

    # --------------------------------------------------------
    # VIEWER REGISTRATION (required by main_organs.py)
    # --------------------------------------------------------
    def register_viewer(self, name, viewer):
        self.viewer_registry[name] = viewer
        return viewer

    # --------------------------------------------------------
    # HEARTBEAT
    # --------------------------------------------------------
    def heartbeat(self):
        self.heartbeat_counter += 1
        packet = {}

        for step in self.pipeline:
            packet = step(packet)

        return packet

    # --------------------------------------------------------
    # RUN LOOP
    # --------------------------------------------------------
    def run(self):
        packet = self.heartbeat()

        # Viewers expect a list of packets
        for name, viewer in self.viewer_registry.items():
            lines = viewer.render([packet])
            for line in lines:
                print(line)
