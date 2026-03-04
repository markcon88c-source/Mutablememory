# creature_state.py

import json
import os

STATE_FILE = "/storage/emulated/0/MutableMemory/critter/snapshot.json"


def save_state(creature):
    """Serialize the creature into a JSON snapshot."""
    data = {
        "heartbeat_count": creature.heartbeat_count,
        "state": creature.state,
        "lfocus": creature.lfocus,

        # Organs with persistence
        "stm": creature.stm.to_dict(),
        "l_levels": creature.l_levels.to_dict(),
        "world": creature.world.to_dict(),
        "story_metrics": creature.story_metrics.to_dict(),

        # Pressure system
        "pressure_core": creature.pressure_core.to_dict(),
        "calm_pressure": creature.calm_pressure.to_dict(),
    }

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_state(CreatureClass):
    """Load creature snapshot if it exists, otherwise return None."""
    if not os.path.exists(STATE_FILE):
        return None

    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return None

    # Create a fresh creature
    creature = CreatureClass()

    # Restore simple fields
    creature.heartbeat_count = data.get("heartbeat_count", 0)
    creature.state = data.get("state", creature.state)
    creature.lfocus = data.get("lfocus", "full")

    # Restore STM
    if "stm" in data:
        creature.stm = creature.stm.__class__.from_dict(data["stm"])

    # Restore L‑Levels
    if "l_levels" in data:
        creature.l_levels = creature.l_levels.__class__.from_dict(data["l_levels"])

    # Restore Story Metrics
    if "story_metrics" in data:
        creature.story_metrics = creature.story_metrics.__class__.from_dict(
            data["story_metrics"]
        )

    # Restore World (requires creature reference)
    if "world" in data:
        creature.world = creature.world.__class__.from_dict(
            data["world"], creature
        )

    # Restore pressure system
    if "pressure_core" in data:
        creature.pressure_core = creature.pressure_core.__class__.from_dict(
            data["pressure_core"]
        )

    if "calm_pressure" in data:
        creature.calm_pressure = creature.calm_pressure.__class__.from_dict(
            data["calm_pressure"]
        )

    return creature
