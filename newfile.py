from mood import MoodOrgan
from drift import DriftOrgan
from worldbuilding import WorldbuildingOrgan
from personality import PersonalityOrgan
from selector import SelectorOrgan
from memory import MemoryOrgan
from longterm_memory import LongTermMemoryOrgan
from english import EnglishOrgan

mood = MoodOrgan()
drift = DriftOrgan()
wb = WorldbuildingOrgan()
personality = PersonalityOrgan()
selector = SelectorOrgan()
memory = MemoryOrgan()
ltm = LongTermMemoryOrgan()
eng = EnglishOrgan()

def run_cycle():
    try:
        current_mood = mood.update()
    except:
        current_mood = ("neutral", {})

    try:
        drift_reason, drift_bool, drift_intensity = drift.compute_drift()
    except:
        drift_reason = "responds"

    try:
        world_packet = wb.generate_many(1)
        world_sample = wb.sample_for_viewer(world_packet)
        if not world_sample:
            world_sample = "the shifting place"
    except:
        world_sample = "the shifting place"

    try:
        verb_optimized = selector.choose()
        if not verb_optimized or verb_optimized == "none":
            verb_optimized = "moves"
    except:
        verb_optimized = "moves"

    try:
        mem_packet = memory.forward([0], [0])
        mem_view = memory.sample_for_viewer(mem_packet)
    except:
        mem_view = "memory: none"

    try:
        ltm_state = ltm.update()
    except:
        ltm_state = "ltm: none"

    try:
        english_out = eng.generate_sentence(
            verb=verb_optimized,
            reaction=drift_reason,
            world=world_sample,
            mood=current_mood
        )
    except:
        english_out = "none"

    return {
        "mood": current_mood,
        "drift": drift_reason,
        "world": world_sample,
        "persona": "none",
        "selection": verb_optimized,
        "memory": mem_view,
        "ltm": ltm_state,
        "english": english_out
    }
