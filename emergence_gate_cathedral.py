import random

FORCE_TYPES = ["calm", "storm", "symbolic", "alert", "concentration"]

FORCE_TARGETS = {
    "calm": 0.30,
    "storm": 0.45,
    "symbolic": 0.40,
    "alert": 0.35,
    "concentration": 0.50,
}

MIN_A1_TICKS = 5
A3_TRIAL_TICKS = 10
A4_CONTEXT_THRESHOLD = 0.6


class BackstageItem:
    def __init__(self, name, letters, mode, origin_block_id, parent_block_ids,
                 force_type, force_value, force_target):
        self.name = name
        self.letters = letters
        self.mode = mode
        self.origin_block_id = origin_block_id
        self.parent_block_ids = parent_block_ids

        self.force_type = force_type
        self.force_value = force_value
        self.force_target = force_target

        self.chamber = "A1"
        self.ticks_in_chamber = 0

        self.context_score = 0.0
        self.trial_ticks = 0

    def __repr__(self):
        return (f"<BackstageItem {self.name} "
                f"ch={self.chamber} force={self.force_type}:{self.force_value:.2f} "
                f"ctx={self.context_score:.2f}>")


class Backstage:
    def __init__(self, creature):
        self.creature = creature
        self.items = []

    # -------------------------------------------------
    # EMERGENCE GATE
    # -------------------------------------------------
    def receive_from_emergence_gate(self, name, block, parent_blocks):
        force_type = random.choice(FORCE_TYPES)
        force_value = random.uniform(0.05, 0.15)
        force_target = FORCE_TARGETS[force_type]

        origin_block_id = block.id if hasattr(block, "id") else None
        parent_block_ids = [b.id for b in parent_blocks if hasattr(b, "id")]

        item = BackstageItem(
            name=name,
            letters=getattr(block, "letters", []),
            mode=getattr(block, "mode", None),
            origin_block_id=origin_block_id,
            parent_block_ids=parent_block_ids,
            force_type=force_type,
            force_value=force_value,
            force_target=force_target,
        )
        self.items.append(item)
        print(f"[EMERGENCE] {item}")
        return item

    # -------------------------------------------------
    # TICK
    # -------------------------------------------------
    def tick(self):
        for item in list(self.items):
            item.ticks_in_chamber += 1

            if item.chamber == "A1":
                self._tick_A1(item)
            elif item.chamber == "A2":
                self._tick_A2(item)
            elif item.chamber == "A3":
                self._tick_A3(item)
            elif item.chamber == "A4":
                self._tick_A4(item)

    # -------------------------------------------------
    # A1 — NURSERY
    # -------------------------------------------------
    def _tick_A1(self, item):
        if item.ticks_in_chamber >= MIN_A1_TICKS:
            item.chamber = "A2"
            item.ticks_in_chamber = 0
            print(f"[A1→A2] {item.name}")

    # -------------------------------------------------
    # A2 — INTERACTION POOL (learning + force growth)
    # -------------------------------------------------
    def _tick_A2(self, item):
        delta = self._apply_force_trial(item, mild=True)
        item.force_value = max(0.0, item.force_value + delta)

        if item.force_value >= item.force_target:
            item.chamber = "A3"
            item.ticks_in_chamber = 0
            item.trial_ticks = 0
            print(f"[A2→A3] {item.name} reached target {item.force_value:.2f}")

        elif item.force_value < 0.02:
            item.chamber = "A1"
            item.ticks_in_chamber = 0
            print(f"[A2→A1] {item.name} regressed")

    # -------------------------------------------------
    # A3 — CRUCIBLE (force‑specific trials)
    # -------------------------------------------------
    def _tick_A3(self, item):
        delta = self._apply_force_trial(item, mild=False)
        item.force_value = max(0.0, item.force_value + delta)
        item.trial_ticks += 1

        if item.trial_ticks >= A3_TRIAL_TICKS:
            self._resolve_A3_choice(item)

        elif item.force_value < 0.05:
            item.chamber = "A2"
            item.ticks_in_chamber = 0
            item.trial_ticks = 0
            print(f"[A3→A2] {item.name} failed trial")

    def _resolve_A3_choice(self, item):
        if item.force_value >= item.force_target * 1.1:
            self._attempt_stm_direct(item)
        else:
            item.chamber = "A4"
            item.ticks_in_chamber = 0
            item.trial_ticks = 0
            print(f"[A3→A4] {item.name} chose Sentence Pool")

    # -------------------------------------------------
    # A4 — SENTENCE POOL (context growth)
    # -------------------------------------------------
    def _tick_A4(self, item):
        # humility: raw force slowly decays
        item.force_value = max(0.0, item.force_value - 0.01)

        # context grows via sentence exposure
        ctx_delta = random.uniform(0.01, 0.05)
        item.context_score = min(1.0, item.context_score + ctx_delta)

        if item.context_score >= A4_CONTEXT_THRESHOLD:
            self._attempt_stm_sentence(item)

        elif item.context_score < 0.05 and item.ticks_in_chamber > 20:
            item.chamber = "A2"
            item.ticks_in_chamber = 0
            print(f"[A4→A2] {item.name} lost context")

    # -------------------------------------------------
    # FORCE TRIALS
    # -------------------------------------------------
    def _apply_force_trial(self, item, mild):
        scale = 0.02 if mild else 0.05

        if item.force_type == "storm":
            # storm grows by calming itself
            spike = random.choice([-1, 1])
            return -scale if spike > 0 else +scale

        if item.force_type == "calm":
            # calm grows by staying steady under pressure
            pressured = random.random() < 0.5
            return +scale if pressured and random.random() < 0.6 else -scale * 0.5

        if item.force_type == "alert":
            # alert grows by picking the right signal
            correct = random.random() < 0.5
            return +scale if correct else -scale

        if item.force_type == "symbolic":
            # symbolic grows by choosing meaningful links
            meaningful = random.random() < 0.5
            return +scale if meaningful else -scale

        if item.force_type == "concentration":
            # concentration grows by staying coherent over time
            stable = random.random() < 0.6
            return +scale if stable else -scale

        return 0.0

    # -------------------------------------------------
    # STM ATTEMPTS
    # -------------------------------------------------
    def _attempt_stm_direct(self, item):
        print(f"[STM-FIGHT] {item.name} force={item.force_value:.2f}")
        accepted = self.creature.stm.try_add_direct(item.name, item.force_value)
        if accepted:
            print(f"[STM-ACCEPT] {item.name} via direct path")
            self.items.remove(item)
        else:
            item.chamber = "A2"
            item.ticks_in_chamber = 0
            item.trial_ticks = 0
            print(f"[STM-REJECT→A2] {item.name}")

    def _attempt_stm_sentence(self, item):
        print(f"[STM-SENTENCE] {item.name} ctx={item.context_score:.2f}")
        accepted = self.creature.stm.try_add_sentence(item.name, item.context_score)
        if accepted:
            print(f"[STM-ACCEPT] {item.name} via sentence path")
            self.items.remove(item)
        else:
            item.chamber = "A4"
            item.ticks_in_chamber = 0
            item.context_score *= 0.5
            print(f"[STM-REJECT stays A4] {item.name}")
