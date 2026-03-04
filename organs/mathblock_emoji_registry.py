# organs/mathblock_emoji_registry.py

import json
import os
import random

REGISTRY_PATH = "mathblock_emoji_registry.json"

# A small pool of emojis to assign
EMOJI_POOL = [
    "🔥", "🌊", "🌱", "⚡", "🌙",
    "🌪️", "🪨", "✨", "🌤️", "🌸",
    "🌀", "💎", "🌟", "🌿", "🌧️"
]


# -----------------------------------------------------
# LOAD REGISTRY
# -----------------------------------------------------
def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {}

    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


# -----------------------------------------------------
# SAVE REGISTRY (JSON‑SAFE)
# -----------------------------------------------------
def save_registry(registry):
    # registry keys MUST be strings for JSON
    safe_registry = {str(k): v for k, v in registry.items()}

    with open(REGISTRY_PATH, "w") as f:
        json.dump(safe_registry, f, indent=2)


# -----------------------------------------------------
# GET EMOJI FOR A MATHBLOCK
# -----------------------------------------------------
def get_emoji_for_mathblock(block):
    """
    Returns an emoji for a MathBlock.
    Ensures JSON‑safe registry keys (string block IDs).
    """

    registry = load_registry()

    block_id = str(block.id)   # JSON‑safe key

    if block_id in registry:
        return registry[block_id]

    # Assign a new emoji
    emoji = random.choice(EMOJI_POOL)
    registry[block_id] = emoji

    save_registry(registry)

    return emoji
