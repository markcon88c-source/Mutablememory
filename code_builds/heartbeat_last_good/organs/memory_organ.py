from decimal import Decimal, getcontext

getcontext().prec = 24

class MemoryOrgan:
    def __init__(self):
        self.words = []
        self.last_words = []

    def _d(self, v):
        return Decimal(str(v))

    def _base_meaning(self, w):
        n = len(w)
        return Decimal(n) / Decimal("20.0")

    def _resonance(self, w, heart):
        h = heart.get("pulse", 0.0)
        v = Decimal(str(h))
        n = Decimal(len(w))
        return (n * v) % Decimal("1.000000000000000")

    def _polarity(self, w, world):
        s = world.get("tone", 0.0)
        v = Decimal(str(s))
        n = Decimal(len(w))
        p = (n * v) % Decimal("2.000000000000000")
        return p - Decimal("1.000000000000000")

    def _cross_influence(self, items):
        out = []
        for i in items:
            m = i["meaning"]
            r = i["resonance"]
            p = i["polarity"]
            for j in items:
                if i is j:
                    continue
                if i["word"][0] == j["word"][0]:
                    m += Decimal("0.0003")
                if i["word"][-1] == j["word"][-1]:
                    r += Decimal("0.0002")
                if len(i["word"]) == len(j["word"]):
                    p += Decimal("0.0001")
            i["meaning"] = m
            i["resonance"] = r
            i["polarity"] = p
            out.append(i)
        return out

    def step(self, thought, world, heart):
        out = []
        words = thought.get("words", [])

        for w in words:
            m = self._base_meaning(w)
            r = self._resonance(w, heart)
            p = self._polarity(w, world)

            out.append({
                "word": w,
                "meaning": m,
                "resonance": r,
                "polarity": p
            })

        out = self._cross_influence(out)
        self.last_words = self.words
        self.words = out
        return self.words
