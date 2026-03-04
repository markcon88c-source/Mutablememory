# ============================================================
# EXPERIMENTAL IMPORT WALL — UNIFIED (CURATED DEFAULT)
# ============================================================

# ------------------------------------------------------------
# VIEWERS
# ------------------------------------------------------------
from viewer.l_level_viewer import LLevelViewer
from viewer.sentence_viewer import SentenceViewer
from viewer.language_viewer import LanguageViewer
from viewer.ocean_space_viewer import OceanSpaceViewer
from viewer.diagnostic_viewer import DiagnosticViewer
from viewer.stm_gravity_viewer import STMGravityViewer
from viewer.stm_integrity_viewer import STMIntegrityViewer
from viewer.symbolic_pressure_viewer import SymbolicPressureViewer
from viewer.universal_viewer import UniversalViewer
from viewer.story_viewer import StoryViewer
from viewer.world_viewer import WorldViewer
from viewer.heart_viewer import HeartViewer
from viewer.cathedral_viewer import CathedralViewer
from viewer.character_birth_viewer import CharacterBirthViewer
from viewer.viewer_registry_class import ViewerRegistry
from viewer.viewer_orchestrator import ViewerOrchestrator
from viewer.viewer_governor import ViewerGovernor
from viewer.viewer_translator import ViewerTranslator

from organs.pressure_viewer import PressureViewer

# ------------------------------------------------------------
# CORE + EXPERIMENTAL ORGANS
# ------------------------------------------------------------
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.meaning_organ import MeaningOrgan
from organs.language_organ import LanguageOrgan
from organs.story_organ import StoryOrgan

from organs.vocabulary_organ import VocabularyOrgan
from organs.lexical_organ import LexicalOrgan
from organs.word_organ import WordOrgan

from organs.pressureorgan import PressureOrgan
from organs.symbolic_organ import SymbolicOrgan
from organs.mythic import MythicOrgan

from organs.world_organ import WorldOrgan
from organs.ocean_organ import OceanOrgan
from organs.shore_organ import ShoreOrgan

from organs.stm_spine_organ import STMSpineOrgan
from organs.name_heart import NameHeart
from organs.birth_force_organ import BirthForceOrgan

from organs.viewer_organ import ViewerOrgan
from organs.emergence_gate_cathedral import EmergenceGateCathedral

# Optional organs (walled off)
# from organs.story_metrics_organ import StoryMetricsOrgan
# from organs.world_idea_organ import WorldIdeaOrgan
# from organs.concentration_pressure import ConcentrationPressureOrgan
# from organs.calm_pressure import CalmPressure
# from organs.wound_organ import WoundOrgan

# ------------------------------------------------------------
# STATE SAVE / LOAD
# ------------------------------------------------------------
from critter.creature_state import save_state, load_state
from main_support.main_switcher import switch_to

# ============================================================
# EXPERIMENTAL WALL CLASS
# ============================================================

class ExperimentalWall:
    def __init__(self, creature, mode="curated"):
        self.creature = creature
        self.mode = mode

    def load_all(self):
        organs = {}

        if self.mode == "auto":
            from organs.organ_registry import OrganRegistry
            registry = OrganRegistry()
            organs = registry.load_all(self.creature)

        organs["SentenceBuilderOrgan"] = SentenceBuilderOrgan(self.creature)
        organs["MeaningOrgan"] = MeaningOrgan(self.creature)
        organs["LanguageOrgan"] = LanguageOrgan(self.creature)
        organs["StoryOrgan"] = StoryOrgan(self.creature)

        organs["EmergenceGateCathedral"] = EmergenceGateCathedral()

        organs["VocabularyOrgan"] = VocabularyOrgan(self.creature)
        organs["LexicalOrgan"] = LexicalOrgan(self.creature, organs["VocabularyOrgan"])
        organs["WordOrgan"] = WordOrgan()

        organs["PressureOrgan"] = PressureOrgan()
        organs["SymbolicOrgan"] = SymbolicOrgan(self.creature)
        organs["MythicOrgan"] = MythicOrgan(self.creature)

        organs["WorldOrgan"] = WorldOrgan()
        organs["OceanOrgan"] = OceanOrgan(self.creature)
        organs["ShoreOrgan"] = ShoreOrgan(self.creature)

        organs["STMSpine"] = STMSpineOrgan(self.creature)
        organs["NameHeart"] = NameHeart(self.creature)
        organs["BirthForceOrgan"] = BirthForceOrgan(self.creature)

        organs["ViewerOrgan"] = ViewerOrgan(self.creature)

        return organs

# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "LLevelViewer", "SentenceViewer", "LanguageViewer", "OceanSpaceViewer",
    "DiagnosticViewer", "STMGravityViewer", "STMIntegrityViewer",
    "SymbolicPressureViewer", "UniversalViewer", "StoryViewer",
    "WorldViewer", "HeartViewer", "CathedralViewer", "CharacterBirthViewer",
    "ViewerRegistry", "ViewerOrchestrator", "ViewerGovernor",
    "ViewerTranslator", "PressureViewer", "ViewerOrgan",
    "STMSpineOrgan", "VocabularyOrgan", "NameHeart",
    "BirthForceOrgan", "EmergenceGateCathedral",
    "save_state", "load_state", "switch_to",
    "ExperimentalWall"
]

# ============================================================
# COMPATIBILITY WRAPPERS
# ============================================================

def import_experimental_organs(creature, mode="curated"):
    wall = ExperimentalWall(creature, mode=mode)
    return wall.load_all()

def import_all_organs(creature, mode="curated"):
    wall = ExperimentalWall(creature, mode=mode)
    return wall.load_all()
