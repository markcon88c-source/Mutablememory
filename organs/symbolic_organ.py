# organs/symbolic_organ.py
# Cathedral-era SymbolicOrgan
# Extends the 10-subforce symbolic pressure engine with:
# - concept pairing
# - symbolic resonance physics
# - symbolic packet emission
# - drift/calm/storm modulation

class SymbolicOrgan:
    """
    Symbolic pressure + symbolic binding organ.
    Computes:
      - the 10 symbolic sub‑forces
      - the unified symbolic pressure (0–1)
      - symbolic resonance between concepts
      - emergent symbolic bindings (A + B → AB)
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_symbol = None
        self.last_pair = None

    # ---------------------------------------------------------
    # Sub‑force computation (your original 10-term engine)
    # ---------------------------------------------------------
    def compute_subforces(self, pkt):
        return {
            "pattern_gravity":            pkt.get("pattern_gravity", 0.0),
            "conceptual_compression":     pkt.get("conceptual_compression", 0.0),
            "ritual_lock_in":             pkt.get("ritual_lock_in", 0.0),
            "semantic_anchoring":         pkt.get("semantic_anchoring", 0.0),
            "coherence_binding":          pkt.get("coherence_binding", 0.0),
            "narrative_momentum":         pkt.get("narrative_momentum", 0.0),
            "structural_symmetry":        pkt.get("structuralsymmetry", 0.0),
            "compression_heat":           pkt.get("compression_heat", 0.0),
            "semantic_inhibition":        pkt.get("semantic_inhibition", 0.0),
            "conceptual_crystallization": pkt.get("conceptual_crystallization", 0.0),
        }

    # ---------------------------------------------------------
    # Weighted symbolic formula (your original)
    # ---------------------------------------------------------
    def compute_symbolic(self, f):
        symbolic = (
            0.08 * f["pattern_gravity"] +
            0.10 * f["conceptual_compression"] +
            0.08 * f["ritual_lock_in"] +
            0.08 * f["semantic_anchoring"] +
            0.10 * f["coherence_binding"] +
            0.08 * f["narrative_momentum"] +
            0.08 * f["structural_symmetry"] +
            0.10 * f["compression_heat"] +
            0.15 * f["semantic_inhibition"] +
            0.15 * f["conceptual_crystallization"]
        )
        return max(0.0, min(1.0, symbolic))

    # ---------------------------------------------------------
    # Symbolic resonance physics (Cathedral-era)
    # ---------------------------------------------------------
    def compute_resonance(self, pressures, drift, stability):
        calm = pressures.get("calm", 0.0)
        storm = pressures.get("storm", 0.0)

        drift_mid = 1.0 - abs(drift - 0.5) * 1.6
        drift_mid = max(0.0, min(1.0, drift_mid))

        resonance = (
            calm * 0.35 +
            stability * 0.30 +
            drift_mid * 0.20 +
            (1.0 - storm) * 0.15
        )

        return max(0.0, min(1.0, resonance))

    # ---------------------------------------------------------
    # Concept binding (A + B → AB)
    # ---------------------------------------------------------
    def bind_concepts(self, concepts, resonance):
        if len(concepts) < 2:
            return None

        a = concepts[-1]
        b = concepts[-2]

        if resonance < 0.25:
            return None

        symbol = f"{a}_{b}"
        self.last_pair = (a, b)
        self.last_symbol = symbol

        return {
            "type": "symbolic",
            "pair": (a, b),
            "symbol": symbol,
            "resonance": resonance,
        }

    # ---------------------------------------------------------
    # Main step
    # ---------------------------------------------------------
    def step(self):
        meta = getattr(self.creature, "_last_meta", {})
        pkt = getattr(self.creature, "last_sentence_packet", {}) or {}
        state = getattr(self.creature, "_last_state", {}) or {}

        # 1. compute sub‑forces
        sub = self.compute_subforces(pkt)

        # 2. compute symbolic pressure
        symbolic = self.compute_symbolic(sub)

        # 3. write pressure to meta
        meta["symbolic"] = symbolic
        meta["pressure_symbolic"] = symbolic

        # 4. symbolic resonance
        pressures = state.get("pressures", {}) or {}
        drift = state.get("drift", 0.0)
        stability = state.get("stability", 0.0)

        resonance = self.compute_resonance(pressures, drift, stability)
        meta["symbolic_resonance"] = resonance

        # 5. concept binding
        concepts = state.get("concepts", [])
        packet = self.bind_concepts(concepts, resonance)

        self.creature._last_meta = meta
        return packet or symbolic
