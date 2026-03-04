import random
from decimal import Decimal, getcontext

getcontext().prec = 24

class HeartOrgan:
    def __init__(self):
        self.rng = random.Random()
        self.lexicon = {}
        self.concepts = [
            "warmth", "threshold", "echo", "root",
            "dust", "hollow", "path", "field"
        ]

    def _pulse(self):
        return Decimal(str(self.rng.random()))

    def _tone(self):
        return Decimal(str(self.rng.random()))

    def _cluster(self, pulse):
        length = 3 + int(pulse * 4)
        out = []
        for _ in range(length):
            out.append("U" if self.rng.random() < 0.5 else "W")
        return "".join(out)

    def _phoneme(self, cluster):
        out = []
        for c in cluster:
            if c == "U":
                out.append("u")
            else:
                out.append("w")
        return "".join(out)

    def _mutate_word(self, phoneme):
        w = phoneme
        if self.rng.random() < 0.3:
            w = w.replace("uu", "u")
        if self.rng.random() < 0.3:
            w = w.replace("ww", "w")
        if self.rng.random() < 0.2:
            w = w + "o"
        if self.rng.random() < 0.2:
            w = w + "a"
        return w

    def _concept(self):
        return self.rng.choice(self.concepts)

    def _polarity(self, cluster, tone):
        u_count = cluster.count("U")
        w_count = cluster.count("W")
        ratio = Decimal(u_count - w_count) / Decimal(len(cluster))
        t = tone
        return (ratio + t) % Decimal("2.0") - Decimal("1.0")

    def _resonance(self, cluster, pulse):
        n = Decimal(len(cluster))
        p = pulse
        return (n * p) % Decimal("1.0")

    def step(self, thought, world):
        pulse = self._pulse()
        tone = self._tone()

        cluster = self._cluster(pulse)

        if cluster not in self.lexicon:
            phon = self._phoneme(cluster)
            word = self._mutate_word(phon)
            concept = self._concept()
            pol = self._polarity(cluster, tone)
            res = self._resonance(cluster, pulse)
            self.lexicon[cluster] = {
                "phoneme": phon,
                "word": word,
                "concept": concept,
                "polarity": pol,
                "resonance": res
            }

        entry = self.lexicon[cluster]

        return {
            "pulse": pulse,
            "tone": tone,
            "cluster": cluster,
            "phoneme": entry["phoneme"],
            "word": entry["word"],
            "concept": entry["concept"],
            "polarity": entry["polarity"],
            "resonance": entry["resonance"]
        }
