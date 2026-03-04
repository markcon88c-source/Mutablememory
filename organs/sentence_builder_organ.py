# ============================================================
# SENTENCE BUILDER ORGAN — finalizes sentence packets
# ============================================================

import math

class SentenceBuilderOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.counter = 0

    # --------------------------------------------------------
    # Cosine similarity for resonance
    # --------------------------------------------------------
    def resonance(self, a, b):
        if not a or not b:
            return 0.0
        dot = sum(x*y for x, y in zip(a, b))
        mag_a = math.sqrt(sum(x*x for x in a))
        mag_b = math.sqrt(sum(y*y for y in b))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

    # --------------------------------------------------------
    # Metabolic step — finalize sentence packet
    # --------------------------------------------------------
    def step(self, packet):
        self.counter += 1

        sentence_layer = packet.get("sentence", {})
        text = sentence_layer.get("text", "")
        anchor = sentence_layer.get("anchor")
        gravity = sentence_layer.get("gravity", 0.0)
        forces = packet.get("forces", {})

        # ----------------------------------------------------
        # 1. Pull sentence mathblock from MathBlockOrgan
        # ----------------------------------------------------
        sentence_mb = self.creature.mathblocks.get_sentence_mathblock(text)

        # ----------------------------------------------------
        # 2. Choose character by resonance
        # ----------------------------------------------------
        characters = self.creature.mathblocks.get_character_mathblocks()
        best_char = None
        best_char_res = -1.0

        for name, char_mb in characters.items():
            r = self.resonance(sentence_mb, char_mb)
            if r > best_char_res:
                best_char_res = r
                best_char = name

        # ----------------------------------------------------
        # 3. Choose faction by resonance
        # ----------------------------------------------------
        factions = self.creature.mathblocks.get_faction_mathblocks()
        best_faction = None
        best_faction_res = -1.0

        for name, fac_mb in factions.items():
            r = self.resonance(sentence_mb, fac_mb)
            if r > best_faction_res:
                best_faction_res = r
                best_faction = name

        # ----------------------------------------------------
        # 4. Choose regular word by resonance
        # ----------------------------------------------------
        words = packet.get("lexical", {}).get("words", [])
        best_word = None
        best_word_res = -1.0

        for w in words:
            w_mb = self.creature.mathblocks.get_word_mathblock(w)
            r = self.resonance(sentence_mb, w_mb)
            if r > best_word_res:
                best_word_res = r
                best_word = w

        # ----------------------------------------------------
        # 5. Determine final identity (character, faction, or word)
        # ----------------------------------------------------
        identity_type = None
        identity_name = None
        identity_res = None

        # Compare all three resonance scores
        if best_char_res >= best_faction_res and best_char_res >= best_word_res:
            identity_type = "character"
            identity_name = best_char
            identity_res = best_char_res

        elif best_faction_res >= best_char_res and best_faction_res >= best_word_res:
            identity_type = "faction"
            identity_name = best_faction
            identity_res = best_faction_res

        else:
            identity_type = "word"
            identity_name = best_word
            identity_res = best_word_res

        # ----------------------------------------------------
        # 6. Determine placement flags
        # ----------------------------------------------------
        placement = {
            "is_dialogue": gravity < 0.3,
            "is_action": 0.3 <= gravity < 0.6,
            "is_internal": gravity >= 0.6,
            "is_world_event": anchor in ["world", "sky", "earth"],
        }

        # ----------------------------------------------------
        # 7. Attach final fields to packet
        # ----------------------------------------------------
        packet["mathblock"] = sentence_mb

        packet["identity"] = {
            "type": identity_type,
            "name": identity_name,
            "resonance": identity_res,
        }

        packet["placement"] = placement
        packet["kind"] = "sentence_packet"
        packet["index"] = self.counter

        # ----------------------------------------------------
        # 8. Emit into Packet Bus
        # ----------------------------------------------------
        self.creature.packet_bus.emit(packet)

        return packet
