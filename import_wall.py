# ============================================================
# IMPORT WALL — CENTRALIZED IMPORT CONTROL FOR THE CREATURE
# ============================================================

# ------------------------------------------------------------
# Delegator additions (experimental wall)
# ------------------------------------------------------------
import critter.import_wall_experimental as import_wall_experimental
from critter.import_wall_experimental import *

# ------------------------------------------------------------
# Core creature components
# ------------------------------------------------------------
from organs.organ_registry import OrganRegistry
from organs.universal_bus_organ import UniversalBusOrgan
from organs.packet_bus_organ import PacketBusOrgan
from organs.packet_trace_organ import PacketTraceOrgan
from organs.bus_diagnostic_organ import BusDiagnosticOrgan
from organs.diagnostic_organ import DiagnosticOrgan
from organs.diagnostic_sentence_emitter import DiagnosticSentenceEmitter
from organs.stat_packet_emitter import StatPacketEmitter
from organs.base_packet_source import BasePacketSource
from organs.base_organ import BaseOrgan

# ------------------------------------------------------------
# Sentence + language pipeline
# ------------------------------------------------------------
from organs.sentence_organ import SentenceOrgan
from organs.sentence_builder_organ import SentenceBuilderOrgan
from organs.sentence_engine import SentenceEngine
from organs.language_organ import LanguageOrgan
from organs.meaning_organ import MeaningOrgan

# Backwards compatibility alias
SentenceBuilder = SentenceBuilderOrgan

# ------------------------------------------------------------
# World + narrative organs
# ------------------------------------------------------------
from organs.world_organ import WorldOrgan
from organs.story_organ import StoryOrgan
from organs.story_metrics_organ import StoryMetricsOrgan
from organs.story_type_organ import StoryTypeOrgan
from organs.iteration_organ import IterationOrgan
from organs.world_idea_organ import WorldIdeaOrgan

# ------------------------------------------------------------
# Pressure + metabolic organs
# ------------------------------------------------------------
from organs.pressureorgan import PressureOrgan
from organs.pressure_core import PressureCore
from organs.alert_pressure_organ import AlertPressureOrgan
from organs.concentration_pressure import ConcentrationPressureOrgan
from organs.metabolic_viewer_organ import MetabolicViewerOrgan
from organs.calm_pressure import CalmPressure

# ------------------------------------------------------------
# Symbolic / mythic / oceanic organs
# ------------------------------------------------------------
from organs.symbolic_organ import SymbolicOrgan
from organs.mythic import MythicOrgan
from organs.ocean_organ import OceanOrgan
from organs.shore_organ import ShoreOrgan
from organs.wound_organ import WoundOrgan
from organs.shadow_cycle import ShadowCycleOrgan
from organs.reason_organ import ReasonOrgan

# ------------------------------------------------------------
# Memory + state organs
# ------------------------------------------------------------
from organs.memory_organ import MemoryOrgan
from organs.state_io import StateOrgan

# ------------------------------------------------------------
# Math block system
# ------------------------------------------------------------
from organs.mathblocks import MathBlocks, MathBlock

# Backwards compatibility alias
MathBlocks = MathBlocks

# ------------------------------------------------------------
# Viewer package
# ------------------------------------------------------------
import viewer

# ============================================================
# EXPORTS
# ============================================================
__all__ = [
    # Core
    "OrganRegistry",
    "UniversalBusOrgan",
    "PacketBusOrgan",
    "PacketTraceOrgan",
    "BusDiagnosticOrgan",
    "DiagnosticOrgan",
    "DiagnosticSentenceEmitter",
    "StatPacketEmitter",
    "BasePacketSource",
    "BaseOrgan",

    # Sentence + language
    "SentenceOrgan",
    "SentenceBuilderOrgan",
    "SentenceBuilder",
    "SentenceEngine",
    "LanguageOrgan",
    "MeaningOrgan",

    # World + narrative
    "WorldOrgan",
    "StoryOrgan",
    "StoryMetricsOrgan",
    "StoryTypeOrgan",
    "IterationOrgan",
    "WorldIdeaOrgan",

    # Pressure + metabolic
    "PressureOrgan",
    "PressureCore",
    "AlertPressureOrgan",
    "ConcentrationPressureOrgan",
    "CalmPressure",
    "MetabolicViewerOrgan",

    # Symbolic / mythic / oceanic
    "SymbolicOrgan",
    "MythicOrgan",
    "OceanOrgan",
    "ShoreOrgan",
    "WoundOrgan",
    "ShadowCycleOrgan",
    "ReasonOrgan",

    # Memory + state
    "MemoryOrgan",
    "StateOrgan",

    # Math
    "MathBlock",
    "MathBlocks",

    # Viewer
    "viewer",
]

# ------------------------------------------------------------
# Delegator extension
# ------------------------------------------------------------
__all__ = __all__ + import_wall_experimental.__all__

# ============================================================
# COMPATIBILITY WRAPPER FOR CREATURE_CATHEDRAL
# ============================================================

def import_all_organs(creature):
    """
    Legacy compatibility wrapper.
    CreatureCathedral still calls import_all_organs(),
    so we forward that call to the Experimental Wall.
    """
    return import_wall_experimental.import_all_organs(creature)
