# RESERVOIR ORGAN — CATHEDRAL EDITION
# Stores packets, words, motifs, and emergent vocabulary for the creature.

class ReservoirOrgan:
    def __init__(self, creature, capacity=5000):
        self.creature = creature
        self.capacity = capacity

        # Core reservoirs
        self.words = []          # raw words
        self.packets = []        # packet objects
        self.motifs = []         # motif clusters
        self.metadata = {}       # optional stats

    # -----------------------------
    # WORD STORAGE
    # -----------------------------
    def add_word(self, word):
        if not isinstance(word, str):
            return
        self.words.append(word)
        if len(self.words) > self.capacity:
            self.words.pop(0)

    def get_words(self, n=None):
        if n is None:
            return list(self.words)
        return self.words[-n:]

    # -----------------------------
    # PACKET STORAGE
    # -----------------------------
    def add_packet(self, packet):
        self.packets.append(packet)
        if len(self.packets) > self.capacity:
            self.packets.pop(0)

    def get_packets(self, n=None):
        if n is None:
            return list(self.packets)
        return self.packets[-n:]

    # -----------------------------
    # MOTIF STORAGE
    # -----------------------------
    def add_motif(self, motif):
        self.motifs.append(motif)
        if len(self.motifs) > self.capacity:
            self.motifs.pop(0)

    def get_motifs(self):
        return list(self.motifs)

    # -----------------------------
    # HEARTBEAT
    # -----------------------------
    def tick(self):
        # Could compute stats, but safe to return snapshot
        return {
            "words": len(self.words),
            "packets": len(self.packets),
            "motifs": len(self.motifs),
        }
