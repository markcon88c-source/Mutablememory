from creature.creature import Creature
from organs.vocabulary_organ import VocabularyOrgan
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.language_organ import LanguageOrgan
from organs.sentence_organ import SentenceOrgan
from organs.packet_bus_organ import PacketBusOrgan
from organs.stm_organ import STMOrgan

from viewer.viewer_governor import ViewerGovernor
from viewer.viewer_translator import ViewerTranslator
from viewer.viewer_orchestrator import ViewerOrchestrator
from viewer.loader import load_all


def main():
    creature = Creature()   # ← MUST come first

    # --------------------------------------------------------
    # ORGAN REGISTRATION
    # --------------------------------------------------------
    creature.register("vocabulary", VocabularyOrgan(creature))
    creature.register("builder", SentenceBuilderOrgan(creature))
    creature.register("language", LanguageOrgan(creature))
    creature.register("sentence", SentenceOrgan(creature))
    creature.register("bus", PacketBusOrgan(creature))
    creature.register("stm", STMOrgan(creature))

    # --------------------------------------------------------
    # LOAD ALL VIEWERS
    # --------------------------------------------------------
    viewers = load_all(creature)

    # --------------------------------------------------------
    # REGISTER VIEWERS  ← REQUIRED FOR GOVERNOR + ORCHESTRATOR
    # --------------------------------------------------------
    for name, viewer in viewers.items():
        creature.register_viewer(name, viewer)

    # --------------------------------------------------------
    # GOVERNOR + TRANSLATOR
    # --------------------------------------------------------
    governor = ViewerGovernor(creature)
    translator = ViewerTranslator(creature)

    # --------------------------------------------------------
    # ORCHESTRATOR
    # --------------------------------------------------------
    orchestrator = ViewerOrchestrator(creature, governor, translator)

    # --------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------
    while True:
        packet = creature.heartbeat()
        orchestrator.render(packet)


if __name__ == "__main__":
    main()
