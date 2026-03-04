# organs/flow_viewer_organ.py

class FlowViewerOrgan:
    """
    FLOW VIEWER ORGAN — PRE‑FLOW + VOCAB FLOW
    -----------------------------------------
    Supports:
      - show_preflow()     → raw vocabulary intake
      - show_vocab_flow()  → snapshot-based vocabulary metabolism
    """

    GREEN = "🟢"
    BLUE  = "🔵"   # no words

    def __init__(self, creature):
        self.creature = creature

    # ---------------------------------------------------------
    # ⭐ PRE‑FLOW VIEWER (original method)
    # ---------------------------------------------------------
    def show_preflow(self, vocab):
        """
        Display the pre‑flow stage:
        Vocabulary intake BEFORE MeaningOrgan or Router.
        """

        words = vocab.active_words
        count = len(words)

        print("\n🌬️ PRE‑FLOW (Vocabulary Intake)")
        print("-----------------------------------------")
        print(f"Reservoir size: {len(vocab.reservoir)}")
        print(f"Reservoir index: {vocab.index}")
        print(f"Words pulled this beat: {count}")

        # rarity breakdown
        rarity_counts = {}
        for w in words:
            r = vocab.rarity.get(w["word"], "common")
            rarity_counts[r] = rarity_counts.get(r, 0) + 1

        print("Rarity mix:", rarity_counts)

        # feeding phase
        phase = "FAST FEED" if not vocab.fast_feed_done else "RAMPING"
        print(f"Phase: {phase}")

        # safety color
        if count == 0:
            print(f"Status: {self.BLUE} NO WORDS")
        else:
            print(f"Status: {self.GREEN} WORD FLOW OK")

    # ---------------------------------------------------------
    # ⭐ VOCAB FLOW VIEWER (snapshot-based)
    # ---------------------------------------------------------
    def show_vocab_flow(self, vocab):
        """
        Snapshot-based vocabulary metabolism viewer.
        Uses VocabularyOrgan.get_flow_snapshot().
        """

        snap = vocab.get_flow_snapshot()

        active = snap["active_count"]
        color = self.GREEN if active > 0 else self.BLUE

        print("\n📚 VOCAB FLOW")
        print("──────────────────────────────")
        print(f"Reservoir size: {snap['reservoir_size']}")
        print(f"Active words:   {active} {color}")
        print(f"Index:          {snap['index']}")
        print(f"Fast feed done: {snap['fast_feed_done']}")
        print(f"Ramp meter:     {snap['ramp_meter']:.2f}")
        print(f"Burst meter:    {snap['burst_meter']:.2f}")
        print(f"Jackpot meter:  {snap['jackpot_meter']:.2f}")
