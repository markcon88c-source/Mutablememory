# viewer/viewer_registry_class.py

from viewer.sentence_viewer import SentenceViewer
from viewer.language_viewer import LanguageViewer
from viewer.story_viewer import StoryViewer
from viewer.ocean_space_viewer import OceanSpaceViewer
from viewer.symbolic_pressure_viewer import SymbolicPressureViewer
from viewer.l_level_viewer import LLevelViewer
from viewer.world_viewer import WorldViewer
from viewer.heart_viewer import HeartViewer
from viewer.cathedral_viewer import CathedralViewer
from viewer.stm_gravity_viewer import STMGravityViewer
from viewer.stm_integrity_viewer import STMIntegrityViewer
from viewer.universal_viewer import UniversalViewer
from viewer.character_birth_viewer import CharacterBirthViewer
from viewer.diagnostic_viewer import DiagnosticViewer

class ViewerRegistry:
    """
    Explicit Cathedral-grade viewer registry.
    Only loads real display viewers.
    """

    def __init__(self):
        self.viewer_classes = {
            "sentence": SentenceViewer,
            "language": LanguageViewer,
            "story": StoryViewer,
            "ocean": OceanSpaceViewer,
            "symbolic_pressure": SymbolicPressureViewer,
            "l_level": LLevelViewer,
            "world": WorldViewer,
            "heart": HeartViewer,
            "cathedral": CathedralViewer,
            "stm_gravity": STMGravityViewer,
            "stm_integrity": STMIntegrityViewer,
            "universal": UniversalViewer,
            "character_birth": CharacterBirthViewer,
            "diagnostic": DiagnosticViewer,
        }

    def load_all(self, creature):
        viewers = {}
        for key, cls in self.viewer_classes.items():
            try:
                viewers[key] = cls(creature)
            except TypeError:
                viewers[key] = cls()
        return viewers
