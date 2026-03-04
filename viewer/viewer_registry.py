# ============================================================
# CATHEDRAL VIEWER REGISTRY — CLEAN, PATCHED, NON-CRASHING
# ============================================================

# Core viewers (these files exist)
from viewer.sentence_viewer import SentenceViewer
from viewer.language_viewer import LanguageViewer
from viewer.story_viewer import StoryViewer
from viewer.ocean_viewer import OceanViewer
from viewer.l_level_viewer import LLevelViewer
from viewer.diagnostic_viewer import DiagnosticViewer

# Optional advanced viewers (guarded imports)
try:
    from viewer.world_viewer import WorldViewer
except:
    WorldViewer = None

try:
    from viewer.heart_viewer import HeartViewer
except:
    HeartViewer = None

try:
    from viewer.cathedral_viewer import CathedralViewer
except:
    CathedralViewer = None

try:
    from viewer.stm_gravity_viewer import STMGravityViewer
except:
    STMGravityViewer = None

try:
    from viewer.stm_integrity_viewer import STMIntegrityViewer
except:
    STMIntegrityViewer = None

try:
    from viewer.universal_viewer import UniversalViewer
except:
    UniversalViewer = None

try:
    from viewer.character_birth_viewer import CharacterBirthViewer
except:
    CharacterBirthViewer = None

# Character viewer (lives in organs/)
try:
    from organs.character_viewer import CharacterViewer
except:
    CharacterViewer = None

# Test viewers (optional)
try:
    from viewer.test_sentence_viewer import TestSentenceViewer
except:
    TestSentenceViewer = None

try:
    from viewer.test_language_viewer import TestLanguageViewer
except:
    TestLanguageViewer = None

try:
    from viewer.test_ocean_viewer import TestOceanViewer
except:
    TestOceanViewer = None


# ============================================================
# VIEWER MAP — MAXIMAL, CLEAN, NO MISSING FILES
# ============================================================

VIEWERS = {
    "sentence": SentenceViewer,
    "language": LanguageViewer,
    "story": StoryViewer,
    "ocean": OceanViewer,
    "l_level": LLevelViewer,
    "diagnostic": DiagnosticViewer,
}

# Optional viewers (only added if import succeeded)
if CharacterViewer: VIEWERS["character"] = CharacterViewer
if WorldViewer: VIEWERS["world"] = WorldViewer
if HeartViewer: VIEWERS["heart"] = HeartViewer
if CathedralViewer: VIEWERS["cathedral"] = CathedralViewer
if STMGravityViewer: VIEWERS["stm_gravity"] = STMGravityViewer
if STMIntegrityViewer: VIEWERS["stm_integrity"] = STMIntegrityViewer
if UniversalViewer: VIEWERS["universal"] = UniversalViewer
if CharacterBirthViewer: VIEWERS["character_birth"] = CharacterBirthViewer

# Test viewers
if TestSentenceViewer: VIEWERS["test_sentence"] = TestSentenceViewer
if TestLanguageViewer: VIEWERS["test_language"] = TestLanguageViewer
if TestOceanViewer: VIEWERS["test_ocean"] = TestOceanViewer


# ============================================================
# LOAD ALL — CREATURE-COMPATIBLE
# ============================================================

def load_all(creature):
    viewers = {}
    for name, cls in VIEWERS.items():
        try:
            viewers[name] = cls(creature)
        except TypeError:
            viewers[name] = cls()
    return viewers
