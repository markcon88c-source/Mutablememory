import os
import time
import random


class StoryCombinerViewer:
    def __init__(self, story_type_viewer=None):
        self.story_type_viewer = story_type_viewer
        self.anim_speed = 0.03

    # ---------------------------------------------------------
    # VISUAL HEADER
    # ---------------------------------------------------------
    def _header(self):
        os.system("clear")
        print(" 🔗 STORY COMBINER VIEWER 🔗")
        print("=" * 60)

    # ---------------------------------------------------------
    # FORCE COMPARISON (placeholder)
    # ---------------------------------------------------------
    def _compare_forces(self, f1, f2):
        deltas = {}
        for k in f1:
            deltas[k] = abs(f1[k] - f2[k])
        return deltas

    # ---------------------------------------------------------
    # MERGE TWO STRUCTURES
    # ---------------------------------------------------------
    def _merge_structures(self, s1, s2):
        """
        Simple merge:
        - subject from s1
        - verb from s2
        - object from whichever has stronger echo (longer)
        - modifier blended
        """
        merged = {}

        merged["subject"] = s1["subject"]
        merged["verb"] = s2["verb"]

        if len(s1["object"]) > len(s2["object"]):
            merged["object"] = s1["object"]
        else:
            merged["object"] = s2["object"]

        merged["modifier"] = random.choice([s1["modifier"], s2["modifier"]])

        return merged

    # ---------------------------------------------------------
    # COMBINE TWO (REAL MODE)
    # ---------------------------------------------------------
    def process(self, story_type):
        """
        Pulls two sentences from the same story tube,
        compares forces, merges structures, and returns
        a new combined structure for refinement.
        """

        bucket = self.story_type_viewer.buckets.get(story_type, [])
        if len(bucket) < 2:
            return None

        self._header()

        a, b = random.sample(bucket, 2)

        s1 = a["sentence"]
        s2 = b["sentence"]
        st1 = a["structure"]
        st2 = b["structure"]

        print("📚 Story Type:", story_type)
        print("\n📝 Sentence A:")
        print(" ", s1)
        print("\n📝 Sentence B:")
        print(" ", s2)

        # fake forces for now
        f1 = {k: len(st1[k]) / 10 for k in st1}
        f2 = {k: len(st2[k]) / 10 for k in st2}

        deltas = self._compare_forces(f1, f2)

        print("\n📐 Force Deltas:")
        for k, v in deltas.items():
            print(f"  {k:8}: {v:.2f}")

        merged = self._merge_structures(st1, st2)

        print("\n🔗 Merged Structure:")
        for k, v in merged.items():
            print(f"  {k:8}: {v}")

        print("\nReturning merged structure for refinement...")
        time.sleep(1.5)

        return merged

    # ---------------------------------------------------------
    # COMBINE MANY (STORY GROWTH MODE — SLOW + READABLE)
    # ---------------------------------------------------------
    def combine_many(self, story_type, count=5):
        """
        Pulls multiple sentences from a story tube,
        merges them iteratively, and returns a final
        combined structure for refinement.
        Now with slower pacing so the user can read it.
        """

        bucket = self.story_type_viewer.buckets.get(story_type, [])
        if len(bucket) < 2:
            return None

        count = min(count, len(bucket))
        entries = random.sample(bucket, count)

        structures = [e["structure"] for e in entries]
        merged = structures[0]

        # Visual header
        self._header()
        print(f"📚 Story Type: {story_type}")
        print(f"🧩 Combining {count} sentences...\n")
        time.sleep(1.2)

        # Show each sentence slowly
        for i, e in enumerate(entries, start=1):
            print(f"  {i}. {e['sentence']}")
            time.sleep(1.4)

        print("\n🔗 Beginning iterative merge...\n")
        time.sleep(1.5)

        # Merge step-by-step with pauses
        for i in range(1, len(structures)):
            prev = merged
            nxt = structures[i]

            print(f"🔄 Merge Step {i}:")
            print(f"   A: {prev['subject']} {prev['verb']} {prev['object']} {prev['modifier']}")
            print(f"   B: {nxt['subject']} {nxt['verb']} {nxt['object']} {nxt['modifier']}")
            time.sleep(1.8)

            merged = self._merge_structures(prev, nxt)

            print("   → Result:")
            print(f"     {merged['subject']} {merged['verb']} {merged['object']} {merged['modifier']}\n")
            time.sleep(2.0)

        print("✨ Final Merged Structure:")
        for k, v in merged.items():
            print(f"  {k:8}: {v}")
        time.sleep(2.0)

        print("\nReturning merged structure for refinement...")
        time.sleep(2.0)

        return merged


# ---------------------------------------------------------
# DEMO MODE (runs only when executed directly)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Minimal fake story_type_viewer for testing
    class FakeStoryTypeViewer:
        def __init__(self):
            self.buckets = {
                "mythic": [
                    {
                        "sentence": "The wanderer follows the silver path under fading stars.",
                        "structure": {
                            "subject": "wanderer",
                            "verb": "follows",
                            "object": "the silver path",
                            "modifier": "under fading stars"
                        }
                    },
                    {
                        "sentence": "The oracle whispers truths behind the veil of dawn.",
                        "structure": {
                            "subject": "oracle",
                            "verb": "whispers",
                            "object": "truths",
                            "modifier": "behind the veil of dawn"
                        }
                    },
                    {
                        "sentence": "The river remembers every footstep along its dreaming banks.",
                        "structure": {
                            "subject": "river",
                            "verb": "remembers",
                            "object": "every footstep",
                            "modifier": "along its dreaming banks"
                        }
                    }
                ]
            }

    viewer = StoryCombinerViewer(story_type_viewer=FakeStoryTypeViewer())

    print("\nRunning StoryCombinerViewer demo...\n")
    time.sleep(1.0)

    # Run single merge
    merged_once = viewer.process("mythic")
    print("\nSingle merge result:", merged_once)
    time.sleep(2.0)

    # Run multi-merge
    merged_many = viewer.combine_many("mythic", count=3)
    print("\nFinal multi-merge result:", merged_many)
