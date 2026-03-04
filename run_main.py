import time

from creature.creature import Creature

from organs.vocabulary_organ import VocabularyOrgan
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.sentence_organ import SentenceOrgan
from organs.language_organ import LanguageOrgan
from organs.packet_bus_organ import PacketBusOrgan
from organs.stm_organ import STMOrgan

from viewer.loader import load_all
from viewer.viewer_governor import ViewerGovernor
from viewer.viewer_translator import ViewerTranslator
from viewer.viewer_orchestrator import ViewerOrchestrator


def main():
    # --------------------------------------------------------
    # CREATURE
    # --------------------------------------------------------
    creature = Creature()

    # --------------------------------------------------------
    # ORGAN REGISTRATION
    # --------------------------------------------------------
    creature.register("vocabulary", VocabularyOrgan(creature))
    creature.register("builder", SentenceBuilderOrgan(creature))
    creature.register("sentence", SentenceOrgan(creature))
    creature.register("language", LanguageOrgan(creature))
    creature.register("bus", PacketBusOrgan(creature))
    creature.register("stm", STMOrgan(creature))

    # --------------------------------------------------------
    # LOAD + REGISTER VIEWERS
    # --------------------------------------------------------
    viewers = load_all(creature)
    for name, viewer in viewers.items():
        creature.register_viewer(name, viewer)

    # --------------------------------------------------------
    # GOVERNOR + TRANSLATOR + ORCHESTRATOR
    # --------------------------------------------------------
    governor = ViewerGovernor(creature)
    translator = ViewerTranslator(creature)
    orchestrator = ViewerOrchestrator(creature, governor, translator)

    # --------------------------------------------------------
    # MAIN LOOP — ONLY ONE RENDER PER HEARTBEAT
    # --------------------------------------------------------
    while True:
        packet = creature.heartbeat()
        orchestrator.render(packet)
        time.sleep(1.78)


if __name__ == "__main__":
    main()
