# ============================================================
# VIEWER ORGAN — CATHEDRAL VIEWER RENDERING NODE
# ============================================================

class ViewerOrgan:
    """
    Base viewer organ for Cathedral viewer system.
    Old metabolism used tick(self); Cathedral uses tick(self, creature)
    and returns packets instead of pushing directly.
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_render = None

    # --------------------------------------------------------
    # CATHEDRAL TICK
    # --------------------------------------------------------
    def tick(self, creature):
        """
        Cathedral metabolism:
        - creature calls: organ.tick(self)
        - viewer returns a render packet
        - orchestrator decides how to display it
        """
        render = self.render()

        if render is None:
            return None

        return {
            "source": "viewer_organ",
            "channel": "viewer",
            "kind": "render",
            "payload": render,
        }

    # --------------------------------------------------------
    # RENDERING HOOK
    # --------------------------------------------------------
    def render(self):
        """
        Override in subclasses.
        Should return a string or dict representing the viewer output.
        """
        return self.last_render
