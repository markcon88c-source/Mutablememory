# organs/central_meaning_organ.py

class CentralMeaningOrgan:
    """
    Tier‑2 Meaning Engine.
    Unifies:
      - words
      - forces
      - mathblocks
    into clean packets for the router.
    """

    def __init__(self, creature):
        self.creature = creature
        self.sentence_builder = creature.sentence_builder
        self.mathblocks = creature.mathblocks

    def build_packets(self):
        """
        Returns a list of unified packets:
        {
            "word": str,
            "forces": dict,
            "mathblock": dict,
            "meaning": dict
        }
        """

        # 1) Pull packets from SentenceBuilderOrgan
        if hasattr(self.sentence_builder, "build_packets"):
            packets = self.sentence_builder.build_packets()
        else:
            packets = []

        unified = []

        for p in packets:
            if not isinstance(p, dict):
                continue

            word = p.get("word")
            forces = p.get("forces", {})

            # 2) Attach mathblock
            mb = None
            if isinstance(word, str):
                blk = self.mathblocks.get_block(word)
                if blk:
                    mb = {
                        "symbol": blk.symbol,
                        "category": blk.category,
                        "force": blk.force,
                    }

            # 3) Build meaning stub (Tier‑2)
            meaning = {
                "is_concept": True if mb else False,
                "category": mb["category"] if mb else None,
            }

            unified.append({
                "word": word,
                "forces": forces,
                "mathblock": mb,
                "meaning": meaning,
            })

        return unified
