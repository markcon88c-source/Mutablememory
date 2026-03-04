import time
from organs.thought_organ import ThoughtOrgan
from organs.world_organ import WorldOrgan
from organs.heart_organ import HeartOrgan
from organs.memory_organ import MemoryOrgan
from organs.stm_organ import STMOrgan
from organs.math_block import MathBlock
from organs.sentence_organ import SentenceOrgan

class Critter:
    def __init__(self):
        self.thought = ThoughtOrgan()
        self.world = WorldOrgan()
        self.heart = HeartOrgan()
        self.memory = MemoryOrgan()
        self.math_block = MathBlock()
        self.stm = STMOrgan(self.math_block)
        self.sentence = SentenceOrgan()

    def step(self):
        thought = self.thought.step()
        world = self.world.step(thought)
        heart = self.heart.step(thought, world)
        mem_words = self.memory.step(thought, world, heart)

        word_snaps = []
        for w in mem_words:
            word_snaps.append({
                "word": w.get("word"),
                "meaning": w.get("meaning", 0.0),
                "resonance": w.get("resonance", 0.0),
                "polarity": w.get("polarity", 0.0)
            })

        stm_state = self.stm.step(word_snaps)
        sentence = self.sentence.step(thought, world, heart, mem_words)

        return {
            "thought": thought,
            "world": world,
            "heart": heart,
            "memory": mem_words,
            "stm": stm_state,
            "sentence": sentence
        }

def print_sentence_viewer(state):
    print("\n================= 🫀 TICK =================")
    print("🧠 Thought:", state["thought"])
    print("🌍 World:", state["world"])

    h = state["heart"]
    print("💓 Heart:",
          "cluster:", h["cluster"],
          "word:", h["word"],
          "concept:", h["concept"],
          "pol:", h["polarity"],
          "res:", h["resonance"])

    print("\n🗣️ Sentence:", state["sentence"])

def print_story_viewer(state):
    print("\n================= 🫀 TICK =================")
    print("🧠 Thought:", state["thought"])
    print("🌍 World:", state["world"])

    h = state["heart"]
    print("💓 Heart:",
          "cluster:", h["cluster"],
          "word:", h["word"],
          "concept:", h["concept"],
          "pol:", h["polarity"],
          "res:", h["resonance"])

    print("\n📝 Memory Words:")
    for w in state["memory"]:
        print("  •", w)

    stm = state["stm"]
    print("\n📚 STM Levels:")
    for i, lvl in enumerate(stm["levels"]):
        if i == 0:
            shown = [x["word"] for x in lvl[:5]]
            print("  L1 🟦:", shown, "...")
        elif i == 1:
            print("  L2 🟩:", [x["word"] for x in lvl])
        elif i == 2:
            print("  L3 🟨:", [x["word"] for x in lvl])
        elif i == 3:
            print("  L4 🟧:", [x["word"] for x in lvl])
        elif i == 4:
            print("  L5 🟥:", [x["word"] for x in lvl])
        elif i == 5:
            print("  L6 🟪:", [x["word"] for x in lvl])
        elif i == 6:
            print("  L7 🟫:", [x["word"] for x in lvl])
        elif i == 7:
            print("  L8 ⚪:", [x["word"] for x in lvl])
        elif i == 8:
            print("  L9 ⚫:", [x["word"] for x in lvl])
        elif i == 9:
            print("  L10 ⭐:", [x["word"] for x in lvl])
        elif i == 10:
            print("  L11 🔮:", [x["word"] for x in lvl])

    if stm["story_seeds"]:
        print("\n✨ Story Seeds:", stm["story_seeds"])

def choose_viewer():
    print("Choose viewer mode:")
    print("1 = Sentence Viewer")
    print("2 = Story-Level Viewer")
    choice = input("Enter choice: ").strip()
    if choice == "1":
        return 1
    if choice == "2":
        return 2
    return 1

def main():
    viewer_mode = choose_viewer()
    critter = Critter()

    while True:
        state = critter.step()
        if viewer_mode == 1:
            print_sentence_viewer(state)
        else:
            print_story_viewer(state)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
