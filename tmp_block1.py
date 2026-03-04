# =========================================================
# main.py — Mythic Creature Core (Block 1)
# =========================================================

# -----------------------------
# Organ Imports
# -----------------------------
from organs.mood_organ import MoodOrgan
from organs.control_room_organ import ControlRoomOrgan

from organs.alert_pressure import AlertPressure
from organs.calm_pressure import CalmPressure
from organs.concentration_pressure import ConcentrationPressure
from organs.symbolic_pressure import SymbolicPressure
from organs.storm import StormOrgan
from organs.word_strength_pressure import WordStrengthPressure

from organs.thought_organ import ThoughtOrgan
from organs.verb_organ import VerbOrgan
from organs.reaction_organ import ReactionOrgan
from organs.worldbuilding_organ import WorldbuildingOrgan
from organs.real_world_organ import RealWorldOrgan
from organs.sentence_organ import SentenceOrgan

from organs.stm import STMOrgan

from viewer import Viewer
import time


# =========================================================
# Critter Class
# =========================================================
class Critter:
    def __init__(self):
        # Core emotional + regulatory organs
        self.mood = MoodOrgan()
        self.control_room = ControlRoomOrgan()

        # Pressure organs
        self.alert = AlertPressure()
        self.calm = CalmPressure()
        self.concentration = ConcentrationPressure()
        self.symbolic = SymbolicPressure()
        self.storm = StormOrgan()
        self.word_strength = WordStrengthPressure()

        # Cognitive + linguistic organs
        self.thought = ThoughtOrgan()
        self.verb = VerbOrgan()
        self.reaction = ReactionOrgan()
        self.world = WorldbuildingOrgan()
        self.real = RealWorldOrgan()
        self.english = SentenceOrgan()

        # Memory organ
        self.stm = STMOrgan()

        # Drift + heartbeat tick
        self.last_valence = 0.5
        self.tick = 0

