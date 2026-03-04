import random

class SentenceOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.bus = creature.bus
        self.last_packet = None

    # ------------------------------------------------------------
    # Bus interface
    # ------------------------------------------------------------
    def receive(self, packet):
        self.last_packet = packet

    # ------------------------------------------------------------
    # Choose part-of-speech based on dominant force
    # ------------------------------------------------------------
    def choose_pos(self, forces):
        if not forces:
            return "noun"

        dominant = max(forces, key=forces.get)

        if dominant == "spark":
            return "verb"
        if dominant == "drift":
            return "adjective"
        if dominant == "clarity":
            return "noun"
        if dominant == "memory":
            return "modifier"
        if dominant == "pressure":
            return "heavy_noun"
        if dominant == "chaos":
            return random.choice(["verb", "noun", "adjective"])

        return "noun"

    # ------------------------------------------------------------
    # Pick a word from the vocabulary based on POS
    # ------------------------------------------------------------
    def pick_word(self, pos):
        lex = self.creature.vocabulary.lexical_words

        if not lex:
            return "shape"

        if pos == "verb":
            verbs = [w for w in lex if w.endswith("s")]
            return random.choice(verbs or lex)

        if pos == "noun":
            nouns = [w for w in lex if w not in ["is", "has"]]
            return random.choice(nouns or lex)

        if pos == "adjective":
            adjs = [w for w in lex if "-" in w or w.endswith("ed")]
            return random.choice(adjs or lex)

        if pos == "modifier":
            mods = [w for w in lex if w.endswith("ly")]
            return random.choice(mods or lex)

        if pos == "heavy_noun":
            heavies = [w for w in lex if w in ["pillar", "stone", "gate", "tower", "monolith"]]
            return random.choice(heavies or lex)

        return random.choice(lex)

    # ------------------------------------------------------------
    # Clarity‑driven fallback sentence generator
    # ------------------------------------------------------------
    def build_fallback_sentence(self, anchor, forces):
        safe_anchor = anchor if isinstance(anchor, str) and anchor.strip() else "shape"

        # Extract clarity force (default 0.0)
        clarity = 0.0
        if isinstance(forces, dict):
            clarity = forces.get("clarity", 0.0)

        words = []

        # -----------------------------
        # MODE 1 — HIGH CLARITY
        # -----------------------------
        if clarity >= 0.35:
            words.append("the")
            words.append(safe_anchor)

            verb = self.pick_word("verb")
            adj = self.pick_word("adjective")
            noun = self.pick_word("noun")
            adv = self.pick_word("modifier")

            words.extend([verb, adj, noun, adv])
            words.append(".")

        # -----------------------------
        # MODE 2 — MEDIUM CLARITY
        # -----------------------------
        elif clarity >= 0.15:
            words.append("the")
            words.append(safe_anchor)

            verb = self.pick_word("verb")
            noun = self.pick_word("noun")
            adv = self.pick_word("modifier")

            words.extend([verb, noun, adv])
            words.append(".")

        # -----------------------------
        # MODE 3 — LOW CLARITY
        # -----------------------------
        else:
            words.append(safe_anchor)
            for _ in range(3):
                pos = random.choice(["noun", "verb", "adjective"])
                words.append(self.pick_word(pos))
            words.append(".")

        # Build final text (punctuation not spaced)
        sentence = " ".join(words[:-1]).capitalize() + words[-1]

        return sentence, words

    # ============================================================
    # PHONETIC LAYER
    # ============================================================
    def build_phonetics(self, tokens):
        out = {}
        for t in tokens:
            if not isinstance(t, str):
                continue
            ipa = self.phoneticize(t)
            vec = self.phoneme_vector(ipa)
            stress = self.stress_pattern(ipa)
            pressure = self.pressure_curve(vec)
            ptype = self.phoneme_type(ipa)

            out[t] = {
                "ipa": ipa,
                "vector": vec,
                "stress": stress,
                "pressure": pressure,
                "phoneme_type": ptype,
            }
        return out

    def phoneticize(self, word):
        mapping = {
            "a": "ɑ", "e": "ɛ", "i": "ɪ", "o": "ɔ", "u": "ʊ",
            "r": "ɹ", "l": "ɫ", "t": "t̪", "s": "s", "k": "kʰ",
            "p": "p", "b": "b", "d": "d", "g": "g",
            "m": "m", "n": "n",
            "f": "f", "v": "v",
            "h": "h",
            "w": "w", "y": "j",
            "c": "kʰ", "q": "kʰ",
        }
        return "".join(mapping.get(c, c) for c in word.lower())

    def phoneme_vector(self, ipa):
        return [(ord(c) % 32) / 32 for c in ipa if c.isalpha()]

    def stress_pattern(self, ipa):
        vowels = "ɑɛɪɔʊ"
        pattern = []
        for c in ipa:
            if c in vowels:
                pattern.append(1 if len(pattern) == 0 else 0)
        return pattern or [0]

    def pressure_curve(self, vec):
        if not vec:
            return [0.0]
        total = sum(vec)
        if total == 0:
            return [0.0 for _ in vec]
        return [v / total for v in vec]

    def phoneme_type(self, ipa):
        if any(p in ipa for p in ["p", "b", "t", "d", "k", "g"]):
            return "plosive"
        if any(p in ipa for p in ["s", "z", "ʃ", "f", "v"]):
            return "fricative"
        if any(p in ipa for p in ["m", "n", "ŋ"]):
            return "nasal"
        if any(p in ipa for p in ["ɫ", "ɹ", "l", "r"]):
            return "liquid"
        if any(p in ipa for p in ["j", "w"]):
            return "glide"
        if any(p in ipa for p in ["ɑ", "æ"]):
            return "vowel_open"
        if any(p in ipa for p in ["ɪ", "ʊ"]):
            return "vowel_closed"
        if any(p in ipa for p in ["ɛ", "ə", "ɔ"]):
            return "vowel_mid"
        return "unknown"

    # ------------------------------------------------------------
    # Main tick — unified semantic + proto_sentence + recursion
    # ------------------------------------------------------------
    def tick(self):
        packet = self.last_packet
        if not isinstance(packet, dict):
            return None

        ptype = packet.get("type")
        anchor = packet.get("anchor")
        gravity = packet.get("gravity", 0.0)
        forces = packet.get("forces", {})
        proto_tokens = packet.get("proto_tokens", [])

        # ========================================================
        # NEW: Accept recursion-stabilized sentences
        # ========================================================
        if ptype == "recursion_stabilized":
            text = packet["payload"].get("text", "")
            tokens = packet["payload"].get("tokens", [text])

            phonetics = self.build_phonetics(tokens)

            out = {
                "type": "sentence",
                "payload": {
                    "text": text,
                    "tokens": tokens,
                    "anchor": anchor,
                    "forces": forces,
                    "gravity": gravity,
                    "proto_tokens": proto_tokens,
                    "phonetics": phonetics,
                    "fallback": False,
                    "stabilized": True,
                },
                "source": "sentence_organ",
            }

            self.bus.emit(out)
            self.last_packet = None
            return out

        # ========================================================
        # FULL ASCENSION (semantic → sentence)
        # ========================================================
        if ptype == "semantic":
            text = packet.get("proto_language", anchor or "")
            tokens = proto_tokens or [anchor or "∅"]
            phonetics = self.build_phonetics(tokens)

            out = {
                "type": "sentence",
                "payload": {
                    "text": text,
                    "tokens": tokens,
                    "anchor": anchor,
                    "forces": forces,
                    "gravity": gravity,
                    "proto_tokens": proto_tokens,
                    "phonetics": phonetics,
                    "fallback": False,
                },
                "source": "sentence_organ",
            }

            self.bus.emit(out)
            self.last_packet = None
            return out

        # ========================================================
        # PURE BOOTSTRAP FALLBACK (proto_sentence → sentence)
        # ========================================================
        if ptype == "proto_sentence":
            text, tokens = self.build_fallback_sentence(anchor, forces.get(anchor, {}))
            phonetics = self.build_phonetics(tokens)

            fallback_anchor = anchor or tokens[0]
            fallback_proto = proto_tokens or tokens

            if not forces:
                forces = {
                    fallback_anchor: {
                        "spark": 0.3,
                        "drift": 0.2,
                        "clarity": 0.4,
                        "memory": 0.1,
                        "pressure": 0.2,
                        "chaos": 0.1,
                    }
                }

            f = forces[fallback_anchor]
            fallback_gravity = max(
                0.0,
                min(1.0, (f["clarity"] + f["pressure"] - f["chaos"]) / 2),
            )

            out = {
                "type": "sentence",
                "payload": {
                    "text": text,
                    "tokens": tokens,
                    "anchor": fallback_anchor,
                    "forces": forces,
                    "gravity": fallback_gravity,
                    "proto_tokens": fallback_proto,
                    "phonetics": phonetics,
                    "fallback": True,
                },
                "source": "sentence_organ",
            }

            self.bus.emit(out)
            self.last_packet = None
            return out

        # ========================================================
        # LEGACY PROTO LANGUAGE
        # ========================================================
        if ptype == "proto_language":
            text, tokens = self.build_fallback_sentence(anchor, forces.get(anchor, {}))
            phonetics = self.build_phonetics(tokens)

            fallback_anchor = anchor or tokens[0]
            fallback_proto = proto_tokens or tokens

            if not forces:
                forces = {
                    fallback_anchor: {
                        "spark": 0.3,
                        "drift": 0.2,
                        "clarity": 0.4,
                        "memory": 0.1,
                        "pressure": 0.2,
                        "chaos": 0.1,
                    }
                }

            f = forces[fallback_anchor]
            fallback_gravity = max(
                0.0,
                min(1.0, (f["clarity"] + f["pressure"] - f["chaos"]) / 2),
            )

            out = {
                "type": "sentence",
                "payload": {
                    "text": text,
                    "tokens": tokens,
                    "anchor": fallback_anchor,
                    "forces": forces,
                    "gravity": fallback_gravity,
                    "proto_tokens": fallback_proto,
                    "phonetics": phonetics,
                    "fallback": True,
                },
                "source": "sentence_organ",
            }

            self.bus.emit(out)
            self.last_packet = None
            return out

        return None
