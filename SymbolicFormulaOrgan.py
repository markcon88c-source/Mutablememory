class SymbolicFormulaOrgan:
    """
    Computes unified symbolic pressure (0–1)
    from the 10 symbolic sub‑forces.
    """

    def __init__(self, creature):
        self.creature = creature

    def step(self):
        meta = getattr(self.creature, "_last_meta", {})

        # 10 symbolic sub‑forces
        P_g = meta.get("pattern_gravity", 0.0)
        C_c = meta.get("conceptual_compression", 0.0)
        R_l = meta.get("ritual_lock_in", 0.0)
        S_a = meta.get("semantic_anchoring", 0.0)
        C_b = meta.get("coherence_binding", 0.0)
        N_m = meta.get("narrative_momentum", 0.0)
        S_s = meta.get("structural_symmetry", 0.0)
        C_h = meta.get("compression_heat", 0.0)
        S_i = meta.get("semantic_inhibition", 0.0)
        C_r = meta.get("conceptual_crystallization", 0.0)

        # Weighted symbolic formula
        symbolic = (
            0.08 * P_g +
            0.10 * C_c +
            0.08 * R_l +
            0.08 * S_a +
            0.10 * C_b +
            0.08 * N_m +
            0.08 * S_s +
            0.10 * C_h +
            0.15 * S_i +
            0.15 * C_r
        )

        symbolic = max(0.0, min(1.0, symbolic))
        meta["symbolic"] = symbolic
        meta["pressure_symbolic"] = symbolic

        self.creature._last_meta = meta
        return symbolic
