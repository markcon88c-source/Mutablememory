# organs/integrity_viewer.py
# Tier‑2 Integrity Viewer

class IntegrityViewer:
    """
    Shows high‑level packet integrity:
      - packet count
      - average forces
      - stability indicators
    """

    def __init__(self, creature=None):
        self.creature = creature

    # ------------------------------------------------------------
    # PUBLIC: SHOW PACKETS
    # ------------------------------------------------------------
    def show(self, packets):
        if not packets:
            print("\n[IntegrityViewer] No packets.\n")
            return

        print("\n==================== INTEGRITY VIEWER ====================")

        # Packet count
        print(f"Packet Count: {len(packets)}")

        # Compute average forces
        force_sums = {}
        count = len(packets)

        for p in packets:
            forces = p.get("forces", {})
            for k, v in forces.items():
                force_sums[k] = force_sums.get(k, 0) + v

        # Print averages
        print("\nAverage Forces:")
        for k, total in force_sums.items():
            avg = total / count
            print(f"  {k:15s}: {avg:.3f}")

        # Stability indicator (simple)
        avg_pressure = force_sums.get("pressure", 0) / count
        if avg_pressure < 0.3:
            stability = "LOW PRESSURE — calm"
        elif avg_pressure < 0.7:
            stability = "MEDIUM PRESSURE — stable"
        else:
            stability = "HIGH PRESSURE — volatile"

        print(f"\nStability: {stability}")

        print("==========================================================\n")
