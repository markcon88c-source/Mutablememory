# ============================
# QUEST FAMILY — PRESSURE (24 quests)
# ============================

from quest_machine import Quest

def pressure_quests():
    q = {}

    for i in range(1, 25):
        qid = f"P{i:03d}"
        q[qid] = Quest(
            id=qid,
            math_block=f"P * {i}",
            interpretation_block=f"P = {i}",
            quest_text=f"Stabilize pressure anomaly {i} before it ruptures.",
            solver_target={"P": i},
            wound_type="pressure",
            drift_intensity=0.40 + (i % 5) * 0.06
        )

    return q
