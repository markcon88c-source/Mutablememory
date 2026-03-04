# organs/concept_viewer.py
# Emergent Concept Viewer — emoji‑rich, stable, compatible with MeaningOrgan v3

from collections import defaultdict

class ConceptViewer:
    def __init__(self, creature):
        self.creature = creature

        # Storage
        self.words = []                 # raw word entries
        self.pairs = []                 # weirdness pairs
        self.families = defaultdict(list)
        self.morphemes = defaultdict(int)
        self.attractors = defaultdict(list)

        # Emergence tracking
        self.prev_family_count = 0
        self.prev_attractor_count = 0
        self.prev_pair_count = 0

    # ------------------------------------------------------------
    # OBSERVE RAW WORD PACKETS
    # ------------------------------------------------------------
    def observe_word(self, word, force, rarity, glue):
        self.words.append({
            "text": word,
            "force": float(force),
            "rarity": float(rarity),
            "glue": float(glue)
        })

    # ------------------------------------------------------------
    # OBSERVE SENTENCE POOL PACKETS
    # ------------------------------------------------------------
    def observe_sentence_pool(self, pool):
        """
        pool is a list of raw word strings.
        We convert them into simple entries for suffix + pair analysis.
        """

        entries = [{"text": w} for w in pool if isinstance(w, str)]

        # Build suffix families
        for entry in entries:
            word = entry["text"]
            for k in range(2, min(6, len(word))):
                suffix = word[-k:]
                self.families[suffix].append(word)

        # Morpheme productivity
        for suffix, words in self.families.items():
            self.morphemes[suffix] = len(words)

        # Attractor families (clusters ≥ 3)
        for suffix, words in self.families.items():
            if len(words) >= 3:
                self.attractors[suffix] = words

    # ------------------------------------------------------------
    # OPTIONAL PAIR PACKETS
    # ------------------------------------------------------------
    def observe_pair(self, p):
        if "a" in p and "b" in p:
            self.pairs.append({
                "a": p["a"],
                "b": p["b"],
                "score": p.get("score", 0.0)
            })

    # ------------------------------------------------------------
    # EMERGENCE METRICS
    # ------------------------------------------------------------
    def compute_emergence(self):
        family_count = len([v for v in self.families.values() if len(v) >= 2])
        attractor_count = len(self.attractors)
        pair_count = len(self.pairs)

        # Growth indicators
        fam_growth = family_count - self.prev_family_count
        att_growth = attractor_count - self.prev_attractor_count
        pair_growth = pair_count - self.prev_pair_count

        # Save for next cycle
        self.prev_family_count = family_count
        self.prev_attractor_count = attractor_count
        self.prev_pair_count = pair_count

        return {
            "families": family_count,
            "attractors": attractor_count,
            "pairs": pair_count,
            "fam_growth": fam_growth,
            "att_growth": att_growth,
            "pair_growth": pair_growth
        }

    # ------------------------------------------------------------
    # RENDER VIEW
    # ------------------------------------------------------------
    def render_view(self):
        e = self.compute_emergence()

        lines = []
        lines.append("🧬 CONCEPT EMERGENCE VIEWER")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # --------------------------------------------------------
        # EMERGENCE SUMMARY
        # --------------------------------------------------------
        lines.append("\n📈 Emergence Summary")

        fam_bar = "🟦" * min(e["families"], 10)
        att_bar = "🟪" * min(e["attractors"], 10)
        pair_bar = "🟨" * min(e["pairs"], 10)

        lines.append(f"Families:   {e['families']:2d} {fam_bar}")
        lines.append(f"Attractors: {e['attractors']:2d} {att_bar}")
        lines.append(f"Weird Pairs:{e['pairs']:2d} {pair_bar}")

        # Growth indicators
        def growth_symbol(v):
            if v > 0: return "🟢⬆️"
            if v < 0: return "🔻"
            return "⚪"

        lines.append(f"Growth: fam {growth_symbol(e['fam_growth'])} | "
                     f"att {growth_symbol(e['att_growth'])} | "
                     f"pair {growth_symbol(e['pair_growth'])}")

        # --------------------------------------------------------
        # TOP WEIRDNESS PAIRS
        # --------------------------------------------------------
        lines.append("\n🔮 Top Weirdness (stretch × glue × force):")
        if not self.pairs:
            lines.append("(no pairs yet)")
        else:
            top = sorted(self.pairs, key=lambda x: x["score"], reverse=True)[:7]
            for p in top:
                lines.append(f"  {p['a']} ↔ {p['b']}   ({p['score']:.4f})")

        # --------------------------------------------------------
        # MORPHOLOGICAL FAMILIES
        # --------------------------------------------------------
        lines.append("\n🧩 Morphological Families:")
        fams = {k: v for k, v in self.families.items() if len(v) >= 2}
        if not fams:
            lines.append("(no families yet)")
        else:
            for suf, words in sorted(fams.items(), key=lambda x: -len(x[1]))[:7]:
                lines.append(f"  -{suf}: {', '.join(words)}")

        # --------------------------------------------------------
        # ATTRACTOR FAMILIES
        # --------------------------------------------------------
        lines.append("\n🌪️ Attractor Clusters:")
        if not self.attractors:
            lines.append("(no attractors yet)")
        else:
            for suf, words in sorted(self.attractors.items(), key=lambda x: -len(x[1]))[:7]:
                lines.append(f"  -{suf}: {', '.join(words)}")

        lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("✨ END CONCEPT VIEW ✨")

        return "\n".join(lines)

    # ------------------------------------------------------------
    # CYCLE
    # ------------------------------------------------------------
    def cycle(self):
        print(self.render_view())
