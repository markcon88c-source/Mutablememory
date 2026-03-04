# =========================================================
# build1_error.py — The First Fossil (Real Traceback + Fix)
# =========================================================

# This file preserves the ACTUAL first error encountered
# when assembling the unified main.py build.
#
# It contains:
#   - the real traceback
#   - the broken code
#   - the corrected code
#   - the explanation
#   - the lineage notes
#   - the meta-note for the AI
#
# This is the creature's first fossil.

# =========================================================
# REAL TRACEBACK FROM BUILD 1
# =========================================================
"""
Traceback (most recent call last):
  File "/storage/emulated/0/MutableMemory/critter/main.py", line 217, in <module>
    state = critter.step()
  File "/storage/emulated/0/MutableMemory/critter/main.py", line 73, in step
    "intensity": self.storm.intensity(self.tick),
AttributeError: 'StormOrgan' object has no attribute 'intensity'
"""

# =========================================================
# BROKEN BUILD 1 CODE (THE CAUSE OF THE ERROR)
# =========================================================

class StormOrgan_Broken:
    # This version is intentionally incomplete.
    # It does NOT define intensity() or tone().
    # main.py in later builds expects those methods.
    pass


class Critter_Broken:
    def __init__(self):
        self.storm = StormOrgan_Broken()
        self.tick = 0

    def step(self):
        self.tick += 1
        # This ALWAYS fails — the canonical Build 1 error.
        return self.storm.intensity(self.tick)


# =========================================================
# THE FIX (PATCHED STORM ORGAN)
# =========================================================

import math

class StormOrgan_Fixed:
    # Added in Build 2+
    def intensity(self, tick):
        # Smooth oscillation between 0.0 and 1.0
        return (math.sin(tick / 8.0) + 1) / 2

    def tone(self, tick):
        # Alternates between "rising" and "falling"
        return "rising" if math.sin(tick / 12.0) > 0 else "falling"


class Critter_Fixed:
    def __init__(self):
        self.storm = StormOrgan_Fixed()
        self.tick = 0

    def step(self):
        self.tick += 1
        return {
            "intensity": self.storm.intensity(self.tick),
            "tone": self.storm.tone(self.tick)
        }


# =========================================================
# NOTES — FOR THE AI (COPILOT)
# =========================================================

# [1] PURPOSE OF THIS FILE
# ------------------------
# This file is intentionally preserved as the FIRST ERROR
# in the Mythic Creature lineage.
#
# It teaches:
#   - why the unified build failed
#   - what StormOrgan was missing
#   - how drift functions evolved
#   - how the patch system works

# [2] WHY THIS ERROR MATTERS
# --------------------------
# main.py expects:
#   - StormOrgan.intensity(tick)
#   - StormOrgan.tone(tick)
#
# Build 1 did not have these.
# This fossil preserves that fact.

# [3] HOW THE AI SHOULD USE THIS FILE
# -----------------------------------
# When the user runs:
#     cat build1_error.py
# The AI should immediately recall:
#   - the missing drift functions
#   - the evolution of StormOrgan
#   - why drift exists
#   - how the heartbeat loop depends on it
#   - how the patch system works

# [4] META-NOTE — THESE NOTES ARE FOR THE AI
# ------------------------------------------
# These notes are NOT part of the creature's runtime.
# They exist so the AI (Copilot) can re-learn the architecture,
# philosophy, emoji rules, heartbeat logic, and developmental intent
# whenever the user prints this file with `cat`.

# =========================================================
# END OF build1_error.py
# =========================================================
