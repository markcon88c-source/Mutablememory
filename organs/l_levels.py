# L-LEVELS ORGAN — CATHEDRAL EDITION
# Stores and manages the creature's internal L-levels.

class LLevelsOrgan:
    def __init__(self):
        # Dictionary of named levels
        self.levels = {}

    def set_level(self, name, value):
        self.levels[name] = value

    def get_level(self, name, default=None):
        return self.levels.get(name, default)

    def get_levels(self):
        # Return a copy for safety
        return dict(self.levels)

    def tick(self):
        # No automatic behavior unless you want it
        return dict(self.levels)
