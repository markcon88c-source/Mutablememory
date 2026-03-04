#!/usr/bin/env python3
from organs.code_reader.code_reader_organ import get_organ_code
from organs.code_cache.code_cache_organ import CodeCache

# List of ALL organs you want to track
MYTHIC_ORGANS = [
    "pressure_core", "storm", "symbolic_pressure", "alert_pressure",
    "concentration_pressure", "calm_pressure", "word_strength_pressure",
    "drift", "storm_thought", "charge_up", "english", "stm",
    "mythic_grammar", "mythic_cycle", "mythic_horizon",
    "mythic_thought", "mythic_worldbuilding", "mythic_hook",
    "mythic_pressure_interpreter"
]

def refresh_all_code():
    """
    Pulls code for every organ and stores it in a CodeCache.
    """
    cache = CodeCache()

    for organ in MYTHIC_ORGANS:
        code = get_organ_code(organ)
        cache.update(organ, code)

    return cache


def main():
    cache = refresh_all_code()
    print("Refreshed code for:", list(cache.all().keys()))
