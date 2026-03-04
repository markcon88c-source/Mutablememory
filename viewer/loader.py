# ============================================================
# VIEWER LOADER — loads all existing viewers in the project
# ============================================================

from viewer.language_viewer import LanguageViewer
from viewer.sentence_viewer import SentenceViewer
from viewer.world_viewer import WorldViewer
from viewer.story_viewer import StoryViewer
from viewer.pressure_viewer import PressureViewer
from viewer.gravity_viewer import GravityViewer
from viewer.birth_viewer import BirthViewer
from viewer.integrity_viewer import IntegrityViewer
from viewer.heart_viewer import HeartViewer
from viewer.cathedral_viewer import CathedralViewer
from viewer.diagnostic_viewer import DiagnosticViewer
from viewer.universal_viewer import UniversalViewer
from viewer.l_level_viewer import LLevelViewer
from viewer.ocean_viewer import OceanViewer


def load_all(creature):
    """
    Returns a dict of all viewer instances keyed by name.
    The governor and orchestrator expect this structure.
    Only viewers that actually exist in the viewer/ directory
    are included here.
    """

    return {
        "language": LanguageViewer(creature),
        "sentence": SentenceViewer(creature),
        "world": WorldViewer(creature),
        "story": StoryViewer(creature),
        "pressure": PressureViewer(creature),
        "gravity": GravityViewer(creature),
        "birth": BirthViewer(creature),
        "integrity": IntegrityViewer(creature),
        "heart": HeartViewer(creature),
        "cathedral": CathedralViewer(creature),
        "diagnostic": DiagnosticViewer(creature),
        "universal": UniversalViewer(creature),
        "l_level": LLevelViewer(creature),
        "ocean": OceanViewer(creature),
    }
