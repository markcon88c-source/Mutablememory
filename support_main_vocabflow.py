#!/data/data/com.termux/files/usr/bin/python

import time

from organs.vocabulary_organ import VocabularyOrgan
from organs.sentence_builder import SentenceBuilderOrgan
from organs.flow_viewer_organ import FlowViewerOrgan


class VocabFlowHarness:
    """
    FLOW2 HARNESS — Vocabulary → Sentence Packets → Vocab Flow
    ----------------------------------------------------------
    Shows:
      1) VocabularyOrgan.tick()
      2) SentenceBuilderOrgan.build()  (metabolic packets)
      3) Sentence Packet Viewer        (small stats + mathblock msg)
      4) Vocab Flow Viewer             (reservoir + meters)
    """

    def __init__(self):
        # Minimal creature stub
        self.pressures = {}
        self.drift = type("Drift", (), {"intensity": 0.0})()

        # Organs
        self.vocab = VocabularyOrgan(self)
        self.builder = SentenceBuilderOrgan(self)
        self.flow = FlowViewerOrgan(self)

    # ---------------------------------------------------------
    # ⭐ SENTENCE PACKET VIEWER (SMALL VERSION)
    # ---------------------------------------------------------
    def show_sentence_packets(self, packets):
        """
        Show the transformation from active words → metabolic packets.
        Includes minimal stats and short mathblock/metabolic messages.
        """

        print("\n🟪 SENTENCE PACKETS")
        print("──────────────────────────────")

        if not packets:
            print("No packets produced.")
            return

        for i, p in enumerate(packets):
            w   = p.get("word", "")
            fs  = p.get("force_score", 0.0)
            f   = p.get("forces", {})
            mb  = p.get("mathblock", None)
            gl  = p.get("glue", None)
            md  = p.get("mood", None)
            st  = p.get("stability", None)

            # Minimal stats (small version)
            stats = p.get("stats", {})
            weird = stats.get("weirdness", None)
            nov   = stats.get("novelty", None)
            ent   = stats.get("entropy", None)

            print(
                f"[{i:02d}] {w:>14} | "
                f"score={fs:.3f} | "
                f"spark={f.get('spark',0):.2f} "
                f"chaos={f.get('chaos',0):.2f} | "
                f"glue={gl} mood={md} | "
                f"stability={st} | "
                f"mb={mb} | "
                f"stats: w={weird} n={nov} e={ent}"
            )

            # ⭐ Short mathblock message
            if mb:
                print("      → mathblock assigned")
            else:
                print("      → no mathblock")

            # ⭐ Outflow confirmation
            print("      → out to metabolic")

    # ---------------------------------------------------------
    # ⭐ MAIN LOOP
    # ---------------------------------------------------------
    def run(self, ticks=20, delay=0.0):
        """
        Run N ticks of vocab metabolism + sentence building.
        """

        for i in range(ticks):
            print(f"\n=== FLOW TICK {i+1} ===")

            # 1) Vocabulary metabolism
            self.vocab.tick()

            # 2) SentenceBuilder outflow (metabolic packets)
            packets = self.builder.build()

            # 3) Sentence packet viewer
            self.show_sentence_packets(packets)

            # 4) Vocabulary flow viewer
            self.flow.show_vocab_flow(self.vocab)

            if delay > 0:
                time.sleep(delay)


if __name__ == "__main__":
    VocabFlowHarness().run()
