# ============================================================
# VIEWER GOVERNOR — Cathedral Viewer Rotation Brain
# ============================================================

class ViewerGovernor:
    def __init__(self, creature):
        self.creature = creature

        # FIX: use viewer_registry, not creature.viewers
        self.viewer_keys = list(creature.viewer_registry.keys())
        self.index = 0

    def choose_viewer(self):
        if not self.viewer_keys:
            return None

        key = self.viewer_keys[self.index]

        # Advance rotation
        self.index = (self.index + 1) % len(self.viewer_keys)

        # FIX: return viewer instance from viewer_registry
        return self.creature.viewer_registry.get(key)
