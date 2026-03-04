# main_support/main_story.py
# Story Organ Sandbox Main

import time
import random
import sys
import os

# ensure organs/ is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from organs.mathblocks import MathBlocks
from organs.heart_organ import HeartOrgan
from organs.story_seed_organ import StorySeedOrgan
from organs.story_weaver_organ import StoryWeaverOrgan
from organs.story_engine_organ import StoryEngineOrgan
from organs.viewer_organ import TrueViewerOrgan


class StorySupportMain:
    def __init__(self):
        self.heart = HeartOrgan()
        self.mathblocks = MathBlocks()
        self.story_seed = StorySeedOrgan()
        self.weaver = StoryWeaverOrgan()
        self.engine = StoryEngineOrgan()
        self.viewer = TrueViewerOrgan()

    def step(self):
        # Heart tick
        heart_state = self.heart.step("", {})

        # Generate a symbolic "thought"
        thought = random.choice(["ember", "veil", "echo", "fracture", "memory", "path"])
        world = {"shift": random.random()}

        # MathBlocks tick
        mathblock_state = self.mathblocks.step(
            thought=thought,
            world=world,
            heart=heart_state
        )

        # Story seed evaluation tick
        story_seed_state = self.story_seed.step(
            mathblocks_state=mathblock_state,
            heart=heart_state
        )

        # Story weaving tick
        weaver_state = self.weaver.step(story_seed_state)

        # Story engine tick
        engine_state = self.engine.step(weaver_state)

        # Viewer state bundle
        state = {
            "heart": heart_state,
            "mathblocks": mathblock_state,
            "story_seeds": story_seed_state,
            "weaver": weaver_state,
            "engine": engine_state,
            "events": [
                ("story.seeds", {
                    "icon": "📖",
                    "candidates": len(story_seed_state.get("candidates", []))
                })
            ]
        }

        # Viewer tick
        self.viewer.step(state)

    def run(self):
        while True:
            print("📚 Story Tick")
            self.step()
            time.sleep(0.5)


def main():
    StorySupportMain().run()


if __name__ == "__main__":
    main()
