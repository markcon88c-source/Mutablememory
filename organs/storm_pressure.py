# organs/storm_pressure.py
# Modern StormPressure: spiky, decaying, ecology-aware

class StormPressure:
    def __init__(self):
        # Current storm intensity in [0, 1]
        self.value = 0.0

    def update(self, creature):
        """
        Modern StormPressure:
        - spikes when forces are high and chaos is active
        - decays over time
        - is softened by calm
        - is shaped by symbolic density and drift
        """

        # --- 1. Base decay (storm doesn't last forever) ---
        self.value *= 0.88  # slow fade-out

        # --- 2. Read other pressures/forces safely ---
        chaos = getattr(creature, "chaos_pressure", None)
        calm = getattr(creature, "calm_pressure", None)
        symbolic = getattr(creature, "symbolic_pressure", None)

        chaos_val = getattr(chaos, "value", 0.0) if chaos else 0.0
        calm_val = getattr(calm, "value", 0.0) if calm else 0.0
        symbolic_val = getattr(symbolic, "value", 0.0) if symbolic else 0.0

        # Drift lives in forces, not as a pressure
        drift_val = 0.0
        try:
            last_packet = creature.last_sentence_packet
            if last_packet and "forces" in last_packet:
                drift_val = float(last_packet["forces"].get("drift", 0.0))
        except Exception:
            drift_val = 0.0

        # --- 3. Storm spike from force + chaos ---
        force_score = getattr(creature, "last_force_score", 0.0)
        base_spike = 0.0

        # Strong force + chaos → storm ignition
        base_spike += max(0.0, force_score - 0.5) * 0.6
        base_spike += chaos_val * 0.4

        # Symbolic density makes storms more meaningful, not just noisy
        base_spike += symbolic_val * 0.25

        # Drift adds instability: more drift → more storm
        base_spike += max(0.0, drift_val) * 0.15

        # --- 4. Calm softens the spike ---
        calm_factor = 1.0 - (calm_val * 0.5)
        base_spike *= max(0.3, calm_factor)

        # --- 5. Apply spike to current value ---
        self.value += base_spike

        # --- 6. Clamp to [0, 1] ---
        self.value = max(0.0, min(1.0, self.value))

        return self.value

    # Backward compatibility with old API
    def compute(self, state):
        """
        Old interface: compute(state)
        We translate it to update(creature).
        """
        creature = state.get("creature") if isinstance(state, dict) else state
        return self.update(creature)
