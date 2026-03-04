# ============================
# QUEST LIBRARY — MANY QUESTS
# ============================

from quest_machine import Quest

def load_all_quests():
    quests = {}

    # ----------------------------
    # Q001 — Frog Resonance
    # ----------------------------
    quests["Q001"] = Quest(
        id="Q001",
        math_block="7 * F",
        interpretation_block="F = 7",
        quest_text="Swim with seven frogs beneath the violet moon.",
        solver_target={"F": 7},
        wound_type="identity",
        drift_intensity=0.2
    )

    # ----------------------------
    # Q002 — Star Drift
    # ----------------------------
    quests["Q002"] = Quest(
        id="Q002",
        math_block="S + 3",
        interpretation_block="S = 4",
        quest_text="Follow the drifting star until it speaks your name.",
        solver_target={"S": 4},
        wound_type="direction",
        drift_intensity=0.4
    )

    # ----------------------------
    # Q003 — Gremlin Echo
    # ----------------------------
    quests["Q003"] = Quest(
        id="Q003",
        math_block="G - 1",
        interpretation_block="G = chaos",
        quest_text="Listen for the gremlin echo in the abandoned corridor.",
        solver_target={"G": 2},
        wound_type="chaos",
        drift_intensity=0.7
    )

    # ----------------------------
    # Q004 — Memory Thread
    # ----------------------------
    quests["Q004"] = Quest(
        id="Q004",
        math_block="M / 2",
        interpretation_block="M = 10",
        quest_text="Recover the memory thread lost in the wind.",
        solver_target={"M": 10},
        wound_type="memory",
        drift_intensity=0.3
    )

    # ----------------------------
    # Q005 — Pressure Bloom
    # ----------------------------
    quests["Q005"] = Quest(
        id="Q005",
        math_block="P + 1",
        interpretation_block="P = 5",
        quest_text="Stabilize the pressure bloom before it ruptures.",
        solver_target={"P": 5},
        wound_type="pressure",
        drift_intensity=0.5
    )

    # ----------------------------
    # Q006 — Lantern of Clarity
    # ----------------------------
    quests["Q006"] = Quest(
        id="Q006",
        math_block="C * 2",
        interpretation_block="C = 3",
        quest_text="Ignite the lantern of clarity in the fogged valley.",
        solver_target={"C": 3},
        wound_type="clarity",
        drift_intensity=0.25
    )

    # ----------------------------
    # Q007 — Whispering Bridge
    # ----------------------------
    quests["Q007"] = Quest(
        id="Q007",
        math_block="W - 4",
        interpretation_block="W = 9",
        quest_text="Cross the whispering bridge without looking back.",
        solver_target={"W": 9},
        wound_type="fear",
        drift_intensity=0.6
    )

    # ----------------------------
    # Q008 — Ember Counting
    # ----------------------------
    quests["Q008"] = Quest(
        id="Q008",
        math_block="E + 2",
        interpretation_block="E = 5",
        quest_text="Count the embers in the dying fire before dawn.",
        solver_target={"E": 5},
        wound_type="loss",
        drift_intensity=0.35
    )

    # ----------------------------
    # Q009 — River of Doubt
    # ----------------------------
    quests["Q009"] = Quest(
        id="Q009",
        math_block="R / 3",
        interpretation_block="R = 12",
        quest_text="Step into the river of doubt and let it judge you.",
        solver_target={"R": 12},
        wound_type="doubt",
        drift_intensity=0.55
    )

    # ----------------------------
    # Q010 — Shadow Ledger
    # ----------------------------
    quests["Q010"] = Quest(
        id="Q010",
        math_block="X + 1",
        interpretation_block="X = shadow",
        quest_text="Balance the shadow ledger before the eclipse.",
        solver_target={"X": 8},
        wound_type="shadow",
        drift_intensity=0.8
    )

    # ----------------------------
    # Q011 — Echo of the First Word
    # ----------------------------
    quests["Q011"] = Quest(
        id="Q011",
        math_block="V - 2",
        interpretation_block="V = 6",
        quest_text="Seek the echo of the first word spoken by the world.",
        solver_target={"V": 6},
        wound_type="voice",
        drift_intensity=0.4
    )

    # ----------------------------
    # Q012 — Broken Compass
    # ----------------------------
    quests["Q012"] = Quest(
        id="Q012",
        math_block="D * 3",
        interpretation_block="D = 2",
        quest_text="Repair the broken compass that points to forgotten places.",
        solver_target={"D": 2},
        wound_type="direction",
        drift_intensity=0.45
    )

    # ----------------------------
    # Q013 — Gremlin Toll
    # ----------------------------
    quests["Q013"] = Quest(
        id="Q013",
        math_block="G + chaos",
        interpretation_block="G = 1",
        quest_text="Pay the gremlin toll at the crooked gate.",
        solver_target={"G": 1},
        wound_type="chaos",
        drift_intensity=0.9
    )

    # ----------------------------
    # Q014 — Heartstone Pulse
    # ----------------------------
    quests["Q014"] = Quest(
        id="Q014",
        math_block="H / 4",
        interpretation_block="H = 16",
        quest_text="Feel the pulse of the heartstone beneath the mountain.",
        solver_target={"H": 16},
        wound_type="heart",
        drift_intensity=0.2
    )

    # ----------------------------
    # Q015 — Lantern of Regret
    # ----------------------------
    quests["Q015"] = Quest(
        id="Q015",
        math_block="L - 3",
        interpretation_block="L = 9",
        quest_text="Carry the lantern of regret through the silent forest.",
        solver_target={"L": 9},
        wound_type
