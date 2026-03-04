# organs/mythic.py
# Minimal Cathedral-era MythicOrgan
# Provides mythic pressure + symbolic amplification hooks.

class MythicOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.value = 0.0

    def compute(self, state):
        # Mythic pressure rises with symbolic resonance and stability
        pressures = state.get("pressures", {}) or {}
        symbolic = pressures.get("symbolic", 0.0)
        stability = state.get("stability", 0.0)
        drift = state.get("drift", 0.0)

        # Mythic resonance: symbolic meaning + stable drift
        drift_mid = 1.0 - abs(drift - 0.5) * 1.6
        drift_mid = max(0.0, min(1.0, drift_mid))

        mythic = (
            symbolic * 0.6 +
            stability * 0.3 +
            drift_mid * 0.1
        )

        # Clamp
        if mythic < 0.0:
            mythic = 0.0
        if mythic > 1.0:
            mythic = 1.0

        self.value = mythic
        return mythic

    def step(self):
        state = getattr(self.creature, "_last_state", {}) or {}
        return self.compute(state)
