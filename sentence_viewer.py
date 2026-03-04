shutting down.
.../MutableMemory/critter $ cat viewers/sentence_viewer.py
# ============================================================
# SENTENCE VIEWER — FULL-SCREEN CINEMATIC SCROLL + BOTTOM HUD
# ============================================================

class SentenceViewer:
    def __init__(self):
        # STREAMING (scrolling) sentence line
        self.last_sentence = None
        self.last_shape = None
        self.last_stability = None

        # HUD data (static panel)
        self.last_phonetics = None
        self.last_proto_language = None
        self.last_forces = None
        self.last_gravity = None
        self.last_anchor = None
        self.last_proto_tokens = None

        # Recursion HUD fields
        self.last_recursion_pass = 0
        self.last_recursion_ready = False
        self.last_recursion_phon = 0.0
        self.last_recursion_force = 0.0
        self.last_recursion_shape = 0.0
        self.last_recursion_grammar = 0.0
        self.last_recursion_gravity = 0.0
        self.last_recursion_shape_name = "line"

        # Track which packet types have been seen
        self.seen = {
            "sentence": False,
            "proto_sentence": False,
            "lexical": False,
            "ocean": False,
            "language": False,
            "drift": False,
            "stm": False,
            "story": False,
        }

        # Scroll buffer for streaming lines
        self.scroll_lines = []

        # Index for 1‑per‑heartbeat scrolling
        self.stream_index = 0

    # ------------------------------------------------------------
    # Receive packets
    # ------------------------------------------------------------
    def receive(self, packet):
        ptype = packet.get("type")
        if ptype in self.seen:
            self.seen[ptype] = True

        # ------------------------------------------------------------
        # SENTENCE PACKETS
        # ------------------------------------------------------------
        if ptype == "sentence":
            payload = packet.get("payload", {})

            # STREAMING LINE
            self.last_sentence = payload.get("text", "")
            self.last_shape = payload.get("shape", "line")
            self.last_stability = payload.get("stability", 0)

            # HUD DATA
            self.last_phonetics = payload.get("phonetics", {})
            self.last_proto_language = payload.get("pos_map", {})
            self.last_forces = payload.get("forces", {})
            self.last_gravity = payload.get("gravity", 0.0)
            self.last_anchor = payload.get("anchor", None)
            self.last_proto_tokens = payload.get("proto_tokens", [])

            # Add streaming line to scroll buffer
            if self.last_sentence:
                self.scroll_lines.append(f"🌟 {self.last_sentence}")

            return

        # ------------------------------------------------------------
        # RECURSION PACKETS
        # ------------------------------------------------------------
        if ptype == "recursion":
            payload = packet.get("payload", {})

            # STREAMING LINE
            sentence = payload.get("sentence", "")
            if sentence:
                self.scroll_lines.append(f"🔁 {sentence}")

            # HUD FIELDS
            self.last_recursion_pass = payload.get("pass", 0)
            self.last_recursion_ready = payload.get("ready_for_ascension", False)
            self.last_recursion_phon = payload.get("phonetic_stability", 0.0)
            self.last_recursion_force = payload.get("force_stability", 0.0)
            self.last_recursion_shape = payload.get("shape_stability", 0.0)
            self.last_recursion_grammar = payload.get("grammar_force", 0.0)
            self.last_recursion_gravity = payload.get("gravity", 0.0)
            self.last_recursion_shape_name = payload.get("shape", "line")

            return

    # ------------------------------------------------------------
    # Graph helper
    # ------------------------------------------------------------
    def graph_curve(self, curve):
        bars = "▁▂▃▄▅▆▇█"
        out = ""
        for v in curve:
            idx = min(int(v * 8), 7)
            out += bars[idx]
        return out

    # ------------------------------------------------------------
    # STREAM OUTPUT
    # ------------------------------------------------------------
    def render_stream(self):
        if self.stream_index >= len(self.scroll_lines):
            return None

        line = self.scroll_lines[self.stream_index]
        self.stream_index += 1
        return line

    # ------------------------------------------------------------
    # HUD OUTPUT
    # ------------------------------------------------------------
    def render_hud(self):
        if self.last_sentence is None:
            return "[SentenceViewer] …awaiting first sentence…"

        # Stability icon
        stability_map = {0: "🟥", 1: "🟨", 2: "🟩", 3: "💚"}
        icon = stability_map.get(self.last_stability, "🟨")

        shapes = {
            "line": "───────",
            "arc": "╭─────╮",
            "wave": "≈≈≈≈≈≈≈",
            "spike": "ᐊᐅᐊᐅᐊᐅ",
            "mountain": "⛰️⛰️⛰️",
        }
        shape_graph = shapes.get(self.last_shape, "───────")

        out = f"[SentenceViewer HUD {icon}] {shape_graph}"

        # -------------------------
        # PHONETICS
        # -------------------------
        if self.last_phonetics:
            out += "\n\n[Phonetics]"
            for token, ph in self.last_phonetics.items():
                ipa = ph.get("ipa", "")
                vec = ph.get("vector", [])
                stress = ph.get("stress", [])
                pressure = ph.get("pressure", [])
                ptype = ph.get("phoneme_type", "unknown")

                out += f"\n  {token}:"
                out += f"\n    IPA: {ipa}"
                out += f"\n    Type: {ptype}"

                if vec:
                    out += f"\n    Vector: {self.graph_curve(vec)}"
                if pressure:
                    out += f"\n    Pressure: {self.graph_curve(pressure)}"
                if stress:
                    out += f"\n    Stress: {stress}"

        # -------------------------
        # POS MAP
        # -------------------------
        if self.last_proto_language:
            out += "\n\n[POS Map]"
            for token, pos in self.last_proto_language.items():
                out += f"\n  {token}: {pos}"

        # -------------------------
        # DIAGNOSTICS
        # -------------------------
        out += "\n\n[Sentence Diagnostics]"
        out += f"\n  Anchor: {self.last_anchor}"
        out += f"\n  Gravity: {self.last_gravity:.3f}"
        out += f"\n  Proto‑tokens: {len(self.last_proto_tokens)}"

        if self.last_forces:
            out += "\n  Forces:"
            for w, f in self.last_forces.items():
                out += (
                    f"\n    {w}: spark={f.get('spark',0):.2f}, "
                    f"drift={f.get('drift',0):.2f}, clarity={f.get('clarity',0):.2f}, "
                    f"memory={f.get('memory',0):.2f}, pressure={f.get('pressure',0):.2f}, "
                    f"chaos={f.get('chaos',0):.2f}"
                )

        # -------------------------
        # RECURSION STATS
        # -------------------------
        out += "\n\n[Recursion]"
        out += f"\n  Pass: {self.last_recursion_pass}"
        out += f"\n  Gravity: {self.last_recursion_gravity:.3f}"
        out += f"\n  Phonetic stability: {self.last_recursion_phon:.3f}"
        out += f"\n  Force stability: {self.last_recursion_force:.3f}"
        out += f"\n  Shape stability: {self.last_recursion_shape:.3f}"
        out += f"\n  Grammar force: {self.last_recursion_grammar:.3f}"
        out += f"\n  Shape: {self.last_recursion_shape_name}"
        out += f"\n  Ready for ascension: {self.last_recursion_ready}"

        # ============================================================
        # INCURSION READINESS — PROTO‑SEEDED + RECURSION‑AWARE
        # ============================================================

        if self.last_recursion_pass == 0:
            # Proto phonetic stability
            phon = min(1.0, (len(self.last_proto_tokens) or 1) / 7.0)

            # Proto force stability
            if self.last_forces:
                chaos_vals = [f.get("chaos", 0.0) for f in self.last_forces.values()]
                avg_chaos = sum(chaos_vals) / len(chaos_vals)
                force = max(0.0, 1.0 - avg_chaos)
            else:
                force = 0.3

            # Total gravity synthesis
            if self.last_forces:
                clarity_vals = [f.get("clarity", 0.0) for f in self.last_forces.values()]
                pressure_vals = [f.get("pressure", 0.0) for f in self.last_forces.values()]
                chaos_vals = [f.get("chaos", 0.0) for f in self.last_forces.values()]
                gravity = max(
                    0.0,
                    min(
                        1.0,
                        (sum(clarity_vals) + sum(pressure_vals) - sum(chaos_vals))
                        / (len(self.last_forces) * 2.0),
                    ),
                )
            else:
                gravity = self.last_gravity or 0.0

            # Proto shape stability
            shape = 0.5

            # Proto grammar force
            grammar = 0.2 if self.last_anchor is None else 0.35

        else:
            # Recursion mode
            phon = self.last_recursion_phon
            force = self.last_recursion_force
            gravity = self.last_recursion_gravity
            shape = self.last_recursion_shape
            grammar = self.last_recursion_grammar

        readiness = (
            0.20 * phon
            + 0.20 * force
            + 0.20 * gravity
            + 0.20 * shape
            + 0.20 * grammar
        )

        filled = int(readiness * 20)
        bar = "█" * filled + "░" * (20 - filled)

        out += "\n\n[Incursion Readiness]"
        out += f"\n  Score: {readiness:.3f} (threshold 0.85)"
        out += f"\n  Bar:   [{bar}]"
        out += f"\n  Status: {'READY' if readiness >= 0.85 else 'not ready'}"

        # -------------------------
        # ASCENSION
        # -------------------------
        proto_active = False
        full_active = False

        if (
            self.last_sentence
            and self.last_forces
            and not (
                self.seen.get("story")
                or self.seen.get("stm")
                or self.seen.get("ocean")
                or self.seen.get("drift")
            )
        ):
            proto_active = True

        if (
            self.seen.get("story")
            or self.seen.get("stm")
            or self.seen.get("ocean")
        ):
            full_active = True

        out += "\n\n[Ascension]"
        out += f"\n  Proto‑ascension: {'ACTIVE' if proto_active else 'INACTIVE'}"
        out += f"\n  Full ascension:  {'ACTIVE' if full_active else 'INACTIVE'}"

        # -------------------------
        # PACKETS NEEDED
        # -------------------------
        needed = []
        for channel in ["proto_sentence", "ocean", "language", "drift", "stm", "story"]:
            if not self.seen[channel]:
                needed.append(channel)

        if needed:
            out += "\n\n[Packets Needed]"
            for n in needed:
                out += f"\n  - {n}"

        return out
.../MutableMemory/critter $ cp <path/to/file> /sdcard/Download/
bash: path/to/file: No such file or directory
.../MutableMemory/critter $ cp viewers/sentence_viewer.py /sdcard/Download/
.../MutableMemory/critter $ cp viewers/sentence_vi
