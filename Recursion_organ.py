.../MutableMemory/critter $ cat organs/recursion_organ.py
# ============================================================
# RECURSION ORGAN — MATHBLOCK-DRIVEN SHAPE SELECTION + 7-STEP LADDER
# ============================================================

import random

class RecursionOrgan:
    def __init__(self, creature):
        self.bus = creature.bus
        self.creature = creature

        # Core sentence state
        self.current_sentence = None
        self.current_tokens = None
        self.current_forces = None
        self.current_phonetics = None

        # Stability fields
        self.current_gravity = 0.0
        self.current_anchor = None
        self.current_shape = "line"
        self.current_stability = 0.0
        self.shape_history = []

        # Identity placeholders
        self.character_id = None
        self.character_role = None
        self.faction_id = None
        self.faction_name = None

        # Recursion cycle index
        self.pass_index = 0

        # Shape families
        self.shape_categories = {
            "wave": "smooth", "arc": "smooth", "curve": "smooth", "swell": "smooth",
            "spiral": "cyclic", "loop": "cyclic", "coil": "cyclic", "helix": "cyclic",
            "pillar": "rigid", "stone": "rigid", "gate": "rigid", "tower": "rigid", "monolith": "rigid",
            "scatter": "chaotic", "burst": "chaotic", "shard": "chaotic", "flicker": "chaotic",
            "ripple": "echo", "ring": "echo", "echo": "echo", "trace": "echo",
            "eclipse": "legendary", "singularity": "legendary", "crown": "legendary",
            "axis": "legendary", "omen": "legendary",
            "line": "neutral",
        }

        # Rarity tiers
        self.shape_rarity = {
            "wave": "common", "arc": "common", "curve": "common", "swell": "common",
            "loop": "common", "coil": "common", "pillar": "common", "stone": "common",
            "gate": "common", "tower": "common", "ripple": "common", "ring": "common",
            "echo": "common", "trace": "common", "scatter": "common", "burst": "common",
            "shard": "common", "flicker": "common", "line": "common",
            "helix": "uncommon", "monolith": "uncommon",
            "spiral": "rare",
            "axis": "epic", "crown": "epic",
            "eclipse": "legendary", "singularity": "legendary", "omen": "legendary",
        }

        self.rarity_bonus = {
            "common": 0.0,
            "uncommon": 0.05,
            "rare": 0.10,
            "epic": 0.15,
            "legendary": 0.20,
        }

    # ============================================================
    # 7-STEP QUANTIZER
    # ============================================================
    def quantize(self, x):
        if x < 0.15: return 0.00
        if x < 0.30: return 0.15
        if x < 0.45: return 0.30
        if x < 0.60: return 0.45
        if x < 0.75: return 0.60
        if x < 0.90: return 0.75
        return 0.90

    # ------------------------------------------------------------
    # Receive sentence packets
    # ------------------------------------------------------------
    def receive(self, packet):
        if packet.get("type") != "sentence":
            return None

        payload = packet.get("payload", {})

        self.current_sentence = payload.get("text", "")
        self.current_tokens = payload.get("tokens", [])
        self.current_forces = payload.get("forces", {})
        self.current_phonetics = payload.get("phonetics", {})

        self.current_gravity = payload.get("gravity", 0.0)
        self.current_anchor = payload.get("anchor", None)
        self.current_shape = payload.get("shape", "line")
        self.current_stability = payload.get("stability", 0.0)

        self.character_id = payload.get("character_id")
        self.character_role = payload.get("character_role")
        self.faction_id = payload.get("faction_id")
        self.faction_name = payload.get("faction_name")

        self.pass_index = 0
        self.shape_history = [self.current_shape]

    # ------------------------------------------------------------
    # Stability components
    # ------------------------------------------------------------
    def phonetic_stability(self):
        if not self.current_phonetics:
            return 0.0

        pressures = []
        for ph in self.current_phonetics.values():
            p = ph.get("pressure", [])
            if p:
                pressures.extend(p)

        if not pressures:
            return 0.0

        avg = sum(pressures) / len(pressures)
        var = sum((x - avg) ** 2 for x in pressures) / len(pressures)
        return max(0.0, 1.0 - min(var, 1.0))

    def force_stability(self):
        if not self.current_forces:
            return 0.0

        chaos_vals = [f.get("chaos", 0.0) for f in self.current_forces.values()]
        avg_chaos = sum(chaos_vals) / len(chaos_vals)
        return max(0.0, 1.0 - avg_chaos)

    def shape_stability(self):
        if len(self.shape_history) < 3:
            return 0.0

        last3 = self.shape_history[-3:]
        categories = [self.shape_categories.get(s, "neutral") for s in last3]

        best_count = max(categories.count(c) for c in set(categories))

        if best_count == 3:
            base = 1.0
        elif best_count == 2:
            base = 0.66
        elif best_count == 1:
            base = 0.33
        else:
            base = 0.0

        max_bonus = max(self.rarity_bonus.get(self.shape_rarity.get(s, "common"), 0.0) for s in last3)

        return min(1.0, base + max_bonus)

    def grammar_force(self):
        if not self.current_tokens:
            return 0.0

        score = 0.0
        for i in range(len(self.current_tokens) - 1):
            a = self.current_tokens[i]
            b = self.current_tokens[i + 1]
            if isinstance(a, str) and isinstance(b, str):
                if a.lower() in ["the", "a", "an"] and b.isalpha():
                    score += 0.1
                if a.isalpha() and b in [".", "!", "?"]:
                    score += 0.1

        return min(score, 1.0)

    # ------------------------------------------------------------
    # MathBlock-driven shape selection
    # ------------------------------------------------------------
    def choose_shape_from_mathblock(self):
        anchor = self.current_anchor
        if not anchor:
            return "line"

        mb = self.creature.mathblocks.get_block(anchor)
        f = mb.force

        signature = {
            "spark": f,
            "drift": f * 0.8,
            "echo": f * 0.6,
            "chaos": f * 0.4,
            "clarity": f * 0.5,
            "memory": f * 0.7,
            "pressure": f * 0.9,
        }

        dominant = max(signature, key=signature.get)

        if f >= 0.85:
            return random.choice(["eclipse", "singularity", "crown", "axis", "omen"])

        if dominant == "spark" or dominant == "clarity":
            family = ["wave", "arc", "curve", "swell"]
        elif dominant == "drift":
            family = ["spiral", "loop", "coil", "helix"]
        elif dominant == "pressure":
            family = ["pillar", "stone", "gate", "tower", "monolith"]
        elif dominant == "chaos":
            family = ["scatter", "burst", "shard", "flicker"]
        elif dominant == "memory" or dominant == "echo":
            family = ["ripple", "ring", "echo", "trace"]
        else:
            family = ["wave", "spiral", "scatter", "ripple"]

        return random.choice(family)

    # ------------------------------------------------------------
    # Ascension readiness
    # ------------------------------------------------------------
    def ascension_ready(self):
        P = self.quantize(self.phonetic_stability())
        F = self.quantize(self.force_stability())
        G = self.quantize(self.current_gravity)
        H = self.quantize(self.shape_stability())
        GR = self.quantize(self.grammar_force())

        S = 0.20 * P + 0.20 * F + 0.20 * G + 0.20 * H + 0.20 * GR
        return S >= 0.85

    # ------------------------------------------------------------
    # Apply one recursion pass
    # ------------------------------------------------------------
    def apply_pass(self):
        self.current_stability = self.quantize(self.current_stability + 0.05)
        self.current_gravity = self.quantize(self.current_gravity + 0.03)

        self.current_shape = self.choose_shape_from_mathblock()
        self.shape_history.append(self.current_shape)

    # ------------------------------------------------------------
    # Emit recursion packet
    # ------------------------------------------------------------
    def make_packet(self):
        return {
            "type": "recursion",
            "payload": {
                "pass": self.pass_index + 1,
                "sentence": self.current_sentence,
                "tokens": self.current_tokens,
                "forces": self.current_forces,
                "phonetics": self.current_phonetics,
                "stability": self.current_stability,
                "gravity": self.current_gravity,
                "anchor": self.current_anchor,
                "shape": self.current_shape,
                "phonetic_stability": self.quantize(self.phonetic_stability()),
                "force_stability": self.quantize(self.force_stability()),
                "shape_stability": self.quantize(self.shape_stability()),
                "grammar_force": self.quantize(self.grammar_force()),
                "ready_for_ascension": self.ascension_ready(),
                "character_id": self.character_id,
                "character_role": self.character_role,
                "faction_id": self.faction_id,
                "faction_name": self.faction_name,
            }
        }

    # ------------------------------------------------------------
    # Heartbeat step
    # ------------------------------------------------------------
    def step(self):
        if self.current_sentence is None:
            return None

        self.apply_pass()
        packet = self.make_packet()
        self.pass_index += 1

        if not packet["payload"]["ready_for_ascension"]:
            self.bus.emit(packet)
            return packet

        stabilized = {
            "type": "recursion_stabilized",
            "payload": {
                "text": self.current_sentence,
                "tokens": self.current_tokens,
                "forces": self.current_forces,
                "phonetics": self.current_phonetics,
                "gravity": self.current_gravity,
                "anchor": self.current_anchor,
                "shape": self.current_shape,
                "stability": self.current_stability,
            },
            "source": "recursion_organ",
        }

        self.bus.emit(stabilized)
        self.current_sentence = None
        return stabilized

    def tick(self):
        return self.step()
.../MutableMemory/critter $
