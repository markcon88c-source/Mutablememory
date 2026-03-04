# FORCE BUS ORGAN — CATHEDRAL EDITION
# Central routing hub for force packets, safe-tick version.

class ForceBusOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.last_error = None
        self.last_packets = []

    def update(self):
        """
        Optional internal update step.
        Override if needed.
        """
        pass

    def route(self):
        """
        Optional routing step.
        Override if your force system uses routing.
        """
        pass

    def update_forces(self):
        """
        Optional force-update step.
        Override if your system computes force deltas here.
        """
        pass

    def tick(self):
        """
        Cathedral-safe tick.
        Executes update(), route(), and update_forces() if present.
        Never crashes the heartbeat.
        """
        try:
            if hasattr(self, "update"):
                self.update()

            if hasattr(self, "route"):
                self.route()

            if hasattr(self, "update_forces"):
                self.update_forces()

        except Exception as e:
            self.last_error = str(e)
            return None
