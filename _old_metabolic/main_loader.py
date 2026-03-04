# ============================================================
#  MAIN LOADER – v3.0 (Universal Creature Loader)
#  Loads the creature and attaches all organs safely.
#  Works from ANY entrypoint (main.py, vocabforce, tests, etc.)
# ============================================================

import os
import sys

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ------------------------------------------------------------
# IMPORT CREATURE + ORGANS
# ------------------------------------------------------------
from creature import Creature

from organs.sentence_builder import SentenceBuilder
from organs.sentence_viewer import SentenceViewer
from organs.heart import HeartOrgan
from organs.mathblocks import MathBlocks

# Optional organs (only attach if present)
def safe_import(module_name, class_name):
    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    except Exception:
        return None


WorldIdeaOrgan = safe_import("organs.world_idea_organ", "WorldIdeaOrgan")
STMOrgan = safe_import("organs.stm", "STMOrgan")
LLevelsOrgan = safe_import("organs.l_levels", "LLevelsOrgan")
StoryMetricsOrgan = safe_import("organs.story_metrics", "StoryMetricsOrgan")
VocabOrgan = safe_import("organs.vocab", "VocabOrgan")


# ------------------------------------------------------------
#  LOAD CREATURE + ATTACH ORGANS
# ------------------------------------------------------------
def load_creature():
    """
    Creates a creature and attaches all available organs.
    This loader is universal and safe across all entrypoints.
    """

    c = Creature()

    # Core organs
    c.name_heart = HeartOrgan(c)
    c.sentence_builder = SentenceBuilder(c)
    c.sentence_viewer = SentenceViewer(c)
    c.mathblocks = MathBlocks(c)

    # Optional organs (attach only if they exist)
    if STMOrgan:
        c.stm = STMOrgan(c)

    if LLevelsOrgan:
        c.l_levels = LLevelsOrgan(c)

    if StoryMetricsOrgan:
        c.story_metrics = StoryMetricsOrgan(c)

    if WorldIdeaOrgan:
        c.world = WorldIdeaOrgan(c)

    if VocabOrgan:
        c.vocab = VocabOrgan(c)

    return c
