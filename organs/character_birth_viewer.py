# CHARACTER BIRTH VIEWER — CATHEDRAL EDITION
# Displays the creature's birth metadata, lineage, and initialization details.

class CharacterBirthViewer:
    def __init__(self, creature):
        self.creature = creature
        self.snapshot = {}

    def tick(self):
        snap = {}

        # Birth timestamp
        if hasattr(self.creature, "birth_timestamp"):
            try:
                snap["birth_timestamp"] = self.creature.birth_timestamp
            except:
                snap["birth_timestamp"] = None

        # Seed or lineage
        if hasattr(self.creature, "birth_seed"):
            try:
                snap["birth_seed"] = self.creature.birth_seed
            except:
                snap["birth_seed"] = None

        # Initial state
        if hasattr(self.creature, "initial_state"):
            try:
                snap["initial_state"] = dict(self.creature.initial_state)
            except:
                snap["initial_state"] = None

        # General creature state
        if hasattr(self.creature, "state"):
            try:
                snap["current_state"] = dict(self.creature.state)
            except:
                snap["current_state"] = None

        self.snapshot = snap
        return snap

    def show(self):
        return dict(self.snapshot)
