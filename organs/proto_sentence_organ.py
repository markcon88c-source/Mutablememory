# ============================================================
# PROTO SENTENCE ORGAN
# Converts lexical packets into proto-sentence packets.
# Provides proto_tokens, proto_language, anchor, gravity,
# and force hints for SentenceOrgan.
# ============================================================

import random

class ProtoSentenceOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.inbox = []
        self.counter = 0

    # --------------------------------------------------------
    # RECEIVE — listen for lexical packets
    # --------------------------------------------------------
    def receive(self, packet):
        if packet.get("type") == "lexical":
            self.inbox.append(packet)

    # --------------------------------------------------------
    # TICK — emit proto_sentence packets
    # --------------------------------------------------------
    def tick(self):
        if not self.inbox:
            return None

        packet = self.inbox.pop(0)
        self.counter += 1

        lexical = packet.get("lexical", {})
        words = lexical.get("words", [])
        word = lexical.get("word")

        # If no words, fallback
        if not words and not word:
            return None

        # Choose anchor
        anchor = words[0] if words else word

        # Build proto_tokens
        proto_tokens = []
        if words:
            proto_tokens.extend(words)
        if word and word not in proto_tokens:
            proto_tokens.append(word)

        # Build proto_language string
        proto_language = " ".join(proto_tokens)

        # Gravity hint (simple force-based seed)
        force = lexical.get("force", 0.0)
        gravity = min(max(force * 0.5, 0.0), 1.0)

        # Forces passthrough
        forces = packet.get("forces", {})

        # Emit proto_sentence packet
        proto_packet = {
            "type": "proto_sentence",
            "channel": "proto_sentence",
            "payload": {
                "proto_tokens": proto_tokens,
                "proto_language": proto_language,
                "anchor": anchor,
                "gravity": gravity,
                "forces": forces,
                "index": self.counter,
            }
        }

        self.creature.bus.emit(proto_packet)
        return proto_packet
