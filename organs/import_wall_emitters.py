# ============================================================
# EMITTERS WALL — Third Experimental Wall
# Dedicated sandbox for packet emitters and world‑pulse organs.
# Keeps the main Experimental Wall untouched.
# ============================================================

# -----------------------------
# Character identity emitter
# -----------------------------
from .character_emitter_organ import CharacterEmitterOrgan

# -----------------------------
# Faction/worldbuilding emitter
# -----------------------------
from .faction_emitter_organ import FactionEmitterOrgan

# -----------------------------
# Health/vitality emitter
# -----------------------------
from .health_emitter_organ import HealthEmitterOrgan

# -----------------------------
# Ambient/environment emitter
# -----------------------------
from .ambient_emitter_organ import AmbientEmitterOrgan


# ============================================================
# REGISTRY — organs exposed to creature.py
# ============================================================

EMITTERS_WALL = {
    "CharacterEmitterOrgan": CharacterEmitterOrgan,
    "FactionEmitterOrgan": FactionEmitterOrgan,
    "HealthEmitterOrgan": HealthEmitterOrgan,
    "AmbientEmitterOrgan": AmbientEmitterOrgan,
}
