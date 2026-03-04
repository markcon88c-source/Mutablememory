# organs/force_viewer.py
# Simple force viewer for normalized force packets

class ForceViewer:
    def __init__(self, creature):
        self.creature = creature
        self.last_forces = {}

    def receive(self, packets):
        """
        Viewer receives routed packets after normalization + integrity.
        Extract force-related fields and store them.
        """
        force_data = {}

        for p in packets:
            # Only process packets that contain force information
            if (
                "force" in p
                or "normalized_force" in p
                or "raw_force" in p
            ):
                pid = p.get("id", len(force_data))

                force_data[pid] = {
                    "raw_force": p.get("force") or p.get("raw_force"),
                    "normalized_force": p.get("normalized_force"),
                    "integrity": p.get("integrity"),
                    "tags": p.get("tags", []),
                }

        self.last_forces = force_data

    def display(self):
        """
        Simple terminal display for now.
        """
        print("\n=== FORCE VIEWER ===")

        if not self.last_forces:
            print("(no force packets yet)")
            return

        for pid, info in self.last_forces.items():
            print(f"\nPacket {pid}:")
            print(f"  Raw Force:        {info.get('raw_force')}")
            print(f"  Normalized Force: {info.get('normalized_force')}")
            print(f"  Integrity:        {info.get('integrity')}")
            print(f"  Tags:             {info.get('tags')}")
