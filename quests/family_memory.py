# ============================
# QUEST FAMILY — MEMORY (24 quests)
# ============================

from quest_machine import Quest

def memory_quests():
    q = {}

    for i in range(1, 25):
        qid = f"M{i:03d}"
        q[qid] = Quest(
            id=qid,
            math_block=f"M - {i}",
            interpretation_block=f"M = {i * 2}",
            quest_text=f"Recover memory fragment {i} from the orchard of echoes.",
            solver_target={"M": i * 2},
            wound_type="memory",
            drift_intensity=0.30 + (i % 5) * 0.04
        )

    return q
