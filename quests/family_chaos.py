# ============================
# QUEST FAMILY — CHAOS (24 quests)
# ============================

from quest_machine import Quest

def chaos_quests():
    q = {}

    for i in range(1, 25):
        qid = f"X{i:03d}"
        q[qid] = Quest(
            id=qid,
            math_block=f"G + chaos",
            interpretation_block=f"G = {i}",
            quest_text=f"Embrace chaos trial {i} in the gremlin warrens.",
            solver_target={"G": i},
            wound_type="chaos",
            drift_intensity=0.60 + (i % 5) * 0.08
        )

    return q
