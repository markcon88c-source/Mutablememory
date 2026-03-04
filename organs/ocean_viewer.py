class OceanViewerOrgan:
    """
    Cathedral-era Ocean Viewer:
    - monitors drifting sentences
    - evaluates them with 10 pressures
    - optionally sends them to BrushUpViewer
    - reinserts them into MeaningOrgan
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_return = None

    def _f(self, x, default=0.0):
        try:
            return float(x)
        except:
            return default

    # ---------------------------------------------------------
    # Compute the 10-pressure return score
    # ---------------------------------------------------------
    def compute_return_score(self, state):
        p = state.get("pressures", {}) or {}

        calm = self._f(p.get("calm"))
        storm = self._f(p.get("storm"))
        symbolic = self._f(p.get("symbolic"))
        concentration = self._f(p.get("concentration"))
        alert = self._f(p.get("alert"))
        stability = self._f(state.get("stability"))
        drift = self._f(state.get("drift"))
        narrative = self._f(p.get("narrative_momentum"))
        coherence = self._f(p.get("coherence_binding"))
        crystallization = self._f(p.get("conceptual_crystallization"))

        score = (
            calm * 0.12 +
            symbolic * 0.12 +
            concentration * 0.10 +
            alert * 0.08 +
            stability * 0.10 +
            narrative * 0.10 +
            coherence * 0.10 +
            crystallization * 0.10 +
            (1.0 - storm) * 0.10 +
            (1.0 - abs(drift - 0.5) * 2.0) * 0.08
        )

        return max(0.0, min(1.0, score))

    # ---------------------------------------------------------
    # Main step: shoreline logic
    # ---------------------------------------------------------
    def step(self):
        state = getattr(self.creature, "_last_state", {}) or {}
        ocean = state.get("ocean", [])
        if not ocean:
            return None

        # Take the most recent drifting sentence
        sentence = ocean[-1]

        score = self.compute_return_score(state)

        # Path A: direct reinsertion
        if score > 0.75:
            pkt = {
                "type": "meaning",
                "channel": "meaning",
                "payload": sentence,
                "source": "ocean_return",
                "score": score,
            }
            self.creature.organs["meaning_organ"].absorb(pkt)
            self.last_return = pkt
            return pkt

        # Path B: send to BrushUpViewer first
        if score > 0.40:
            brush = self.creature.organs.get("brush_up_viewer")
            if brush:
                polished = brush.polish(sentence)
            else:
                polished = sentence

            pkt = {
                "type": "meaning",
                "channel": "meaning",
                "payload": polished,
                "source": "ocean_brushup",
                "score": score,
            }
            self.creature.organs["meaning_organ"].absorb(pkt)
            self.last_return = pkt
            return pkt

        # Path C: dissolve into concept memory
        concepts = state.get("concepts", [])
        concepts.append(sentence)
        state["concepts"] = concepts
        self.creature._last_state = state

        self.last_return = {
            "type": "dissolve",
            "sentence": sentence,
            "score": score,
        }
        return None
