# ============================
# QUEST FAMILY — CLARITY (24 quests)
# ============================

from quest_machine import Quest

def clarity_quests():
    q = {}

    for i in range(1, 25):
        qid = f"C{i:03d}"
        q[qid] = Quest(
            id=qid,
            math_block=f"C + {i}",
            interpretation_block=f"C = {i}",
            quest_text=f"Seek clarity number {i} in the fog of shifting truths.",
            solver_target={"C": i},
            wound_type="clarity",
            drift_intensity=0.20 + (i % 5) * 0.05
        )

    return q
