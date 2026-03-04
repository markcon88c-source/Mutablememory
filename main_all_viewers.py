import time
from creature.creature import Creature

# Viewer stack
from viewer.viewer_governor import ViewerGovernor
from viewer.viewer_translator import ViewerTranslator
from viewer.viewer_orchestrator import ViewerOrchestrator

# All viewers you currently have
from viewer.sentence_viewer import SentenceViewer
from viewer.language_viewer import LanguageViewer
from viewer.ocean_space_viewer import OceanSpaceViewer
from viewer.diagnostic_viewer import DiagnosticViewer
from viewer.llevel_viewer import LLevelViewer
from viewer.stm_gravity_viewer import STMGravityViewer
from viewer.stm_integrity_viewer import STMIntegrityViewer
from viewer.symbolic_pressure_viewer import SymbolicPressureViewer
from viewer.universal_viewer import UniversalViewer
from viewer.character_birth_viewer import CharacterBirthViewer


def main():
    creature = Creature()

    # Viewer stack
    creature.governor = ViewerGovernor(creature)
    creature.translator = ViewerTranslator()
    creature.viewer = ViewerOrchestrator(creature, creature.governor, creature.translator)

    # Register ALL viewers
    creature.viewers = {
        "sentence": SentenceViewer(creature),
        "language": LanguageViewer(creature),
        "ocean": OceanSpaceViewer(creature),
        "diagnostic": DiagnosticViewer(creature),
        "llevel": LLevelViewer(creature),
        "gravity": STMGravityViewer(creature),
        "integrity": STMIntegrityViewer(creature),
        "pressure": SymbolicPressureViewer(creature),
        "universal": UniversalViewer(creature),
        "birth": CharacterBirthViewer(creature),
    }

    # Heartbeat loop
    while True:
        packet = creature.heartbeat()
        frame = creature.viewer.render(packet)
        if frame:
            print(frame)
        time.sleep(1.78)


if __name__ == "__main__":
    main()
