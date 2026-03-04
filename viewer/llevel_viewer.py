class LLevelViewer:
    def __init__(self, creature):
        self.creature = creature
        self.name = "LLevelViewer"

    def render(self, packet):
        tick = packet.get("tick", 0)

        # If the creature has no L-level organ, show a placeholder
        llevel_value = None
        if hasattr(self.creature, "stm"):
            # If STM organ exposes an L-level metric, use it
            llevel_value = getattr(self.creature.stm, "l_level", None)

        # Build the frame
        frame = []
        frame.append("=== L-LEVEL VIEWER ===")
        frame.append(f"Tick: {tick}")

        if llevel_value is None:
            frame.append("L-Level: (no data)")
        else:
            frame.append(f"L-Level: {llevel_value}")

        return "\n".join(frame)
