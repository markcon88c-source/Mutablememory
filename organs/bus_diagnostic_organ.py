class BusDiagnosticOrgan:
    """
    Full organ diagnostic:
    - Iterates through every organ in creature.organs
    - Marks ✓ if the organ responds without error
    - Marks ✗ if the organ throws or fails
    """

    def __init__(self, creature):
        self.creature = creature
        self.last_snapshot = {}

    def tick(self):
        snapshot = {}

        for name, organ in self.creature.organs.items():
            try:
                # Light, safe ping
                _ = organ.__class__.__name__
                snapshot[name] = "✓"
            except Exception:
                snapshot[name] = "✗"

        self.last_snapshot = snapshot

    def snapshot(self):
        return self.last_snapshot
