# hook.py
# Single hook organ: 1-word English, 2-word Thought

import random

rng = random.Random()

ROOTS = [
    "pulse", "signal", "echo", "thread", "stone",
    "memory", "horizon", "glyph", "fragment", "current"
]

MODIFIERS = [
    "hidden", "restless", "ancient", "unsteady",
    "trembling", "distant", "quiet", "soft", "rising", "sinking"
]


def generate_hook(state):
    symbolic = state.get("pressures", {}).get("symbolic", 0.0)
    alert = state.get("pressures", {}).get("alert", 0.0)
    mood = state.get("mood_state", "calm")
    drift = state.get("drift", "flat")

    # -----------------------------
    # MOOD-BASED IGNITION BOOST
    # -----------------------------
    mood_boost = {
        "calm": 0.02,
        "curious": 0.05,
        "bright": 0.08,
        "focused": 0.06,
        "chaotic": -0.04,
    }.get(mood, 0.02)

    # -----------------------------
    # DRIFT-BASED BOOST
    # -----------------------------
    drift_boost = {
        "up": 0.03,
        "down": 0.01,
        "flat": 0.0,
    }.get(drift, 0.0)

    # -----------------------------
    # IGNITION PROBABILITY
    # -----------------------------
    chance = symbolic - alert + mood_boost + drift_boost

    # variability
    chance += rng.uniform(-0.05, 0.05)

    if chance < 0.0:
        return None

    if rng.random() < chance:
        root = rng.choice(ROOTS)
        modifier = rng.choice(MODIFIERS)
        strength = max(0.0, min(1.0, chance))

        return {
            "root": root,
            "modifier": modifier,
            "strength": strength,
        }

    return None
