# ============================
# QUEST MACHINE — PROTOTYPE
# ============================

from dataclasses import dataclass
from typing import Dict, Any, List
import time
import os
import itertools

# ----------------------------
# Quest Data Structure
# ----------------------------

@dataclass
class Quest:
    id: str
    math_block: str                 # wounded equation
    interpretation_block: str       # math that controls the English line
    quest_text: str                 # English interpretation
    solver_target: Dict[str, Any]   # what the solver sets
    wound_type: str                 # type of wound
    drift: float                    # drift intensity for animation


# ----------------------------
# Quest Machine (mythic hardware)
# ----------------------------

class QuestMachine:
    def __init__(self):
        self.quests: List[Quest] = []

    def add_quest(self, quest: Quest):
        self.quests.append(quest)

    def get(self, quest_id: str) -> Quest:
        for q in self.quests:
            if q.id == quest_id:
                return q
        raise ValueError(f"Quest '{quest_id}' not found")


# ----------------------------
# First-Person Renderer (drifting math + interpretation)
# ----------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def render_first_person(quest: Quest, cycles=20, delay=0.08):
    drift_pattern = [0, 1, 2, 1]  # subtle sway
    drift_cycle = itertools.cycle(drift_pattern)

    for _ in range(cycles):
        offset = next(drift_cycle)
        clear()

        # Top border (the chamber threshold)
        print("╔" + "═" * 58 + "╗")
        print("║" + " QUEST MACHINE — FIRST‑PERSON CHAMBER ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()

        # Math block drifting
        print("  MATH BLOCK:")
        print(" " * (4 + offset) + quest.math_block)
        print()

        # Interpretation block drifting
        print("  INTERPRETATION BLOCK:")
        print(" " * (4 + offset) + quest.interpretation_block)
        print()

        # English interpretation (stable)
        print("  THE CATHEDRAL WHISPERS:")
        print(f"    {quest.quest_text}")
        print()

        # Internal metadata
        print(f"  [wound: {quest.wound_type}]")
        print()

        time.sleep(delay)


# ----------------------------
# Canonical Starter Quests
# ----------------------------

quest_machine = QuestMachine()

quest_machine.add_quest(Quest(
    id="Q001",
    math_block="7 * F",
    interpretation_block="F = 7",
    quest_text="You must swim with 7 frogs.",
    solver_target={"F": 7},
    wound_type="missing_meaning",
    drift=0.12,
))

quest_machine.add_quest(Quest(
    id="Q002",
    math_block="x + 3 = 9",
    interpretation_block="x = 9 - 3",
    quest_text="You must find the number that hides behind the door marked 9.",
    solver_target={"x": 6},
    wound_type="incomplete_identity",
    drift=0.05,
))

quest_machine.add_quest(Quest(
    id="Q003",
    math_block="Δ = 4 - y",
    interpretation_block="y = 4 - Δ",
    quest_text="You must chase the vanishing shadow that subtracts itself from 4.",
    solver_target={"y": "4 - Δ"},
    wound_type="drift_wound",
    drift=0.33,
))

quest_machine.add_quest(Quest(
    id="Q004",
    math_block="S / 2",
    interpretation_block="S = 2 * meaning",
    quest_text="You must divide the silver stone in half without breaking its meaning.",
    solver_target={"S": "2 * meaning"},
    wound_type="force_misalignment",
    drift=0.18,
))

quest_machine.add_quest(Quest(
    id="Q005",
    math_block="R^2 - 1",
    interpretation_block="R = sqrt(1 + circle)",
    quest_text="You must restore the missing circle that was taken from the squared radius.",
    solver_target={"R": "sqrt(1 + circle)"},
    wound_type="confidence_collapse",
    drift=0.44,
))


# ----------------------------
# Example Run
# ----------------------------

if __name__ == "__main__":
    q = quest_machine.get("Q001")
    render_first_person(q)
