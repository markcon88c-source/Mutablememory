# FORCE BUILDER ORGAN — CATHEDRAL EDITION
# Builds and updates force structures each heartbeat.

class ForceBuilderOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.last_error = None
        self.last_forces = {}

    def build_forces(self):
        """
        Core force construction logic.
        Override with real force-building behavior as needed.
        """
        forces = {}

        # Example: derive simple forces from creature.state
        state = getattr(self.creature, "state", {})
        pressure = float(state.get("pressure", 50))
        heartbeat = float(state.get("heartbeat", 0))

        forces["baseline_pressure"] = pressure
        forces["heartbeat_pulse"] = heartbeat % 10

        self.last_forces = forces
        return forces

    def tick(self):
        """
        Cathedral-safe tick.
        Computes forces and stores them; never crashes the heartbeat.
        """
        try:
            return self.build_forces()
        except Exception as e:
            self.last_error = str(e)
            return None
