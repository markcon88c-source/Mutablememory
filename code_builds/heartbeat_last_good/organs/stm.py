class STMOrgan:
    def __init__(self):
        self.max_L1 = 5
        self.max_L2 = 5
        self.max_L3 = 5

    def update(self, state):
        thought = state.get("thought", "")

        # If there's a new thought, push it into L1
        if thought:
            L1 = state["stm"]["L1"]
            L1.append(thought)
            if len(L1) > self.max_L1:
                L1.pop(0)

        # Every few ticks, cascade L1 → L2 → L3
        tick = state.get("tick", 0)
        if tick % 10 == 0:
            L1 = state["stm"]["L1"]
            L2 = state["stm"]["L2"]
            L3 = state["stm"]["L3"]

            if L1:
                L2.append(L1.pop(0))
                if len(L2) > self.max_L2:
                    L2.pop(0)

            if L2:
                L3.append(L2.pop(0))
                if len(L3) > self.max_L3:
                    L3.pop(0)

        # FIX: return the full state, not just STM
        return state
