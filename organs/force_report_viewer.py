# force_report_viewer.py
# ============================================================
# FORCE REPORT VIEWER
# Displays a structured, readable report of force packets.
# ============================================================

class ForceReportViewer:
    def __init__(self, creature):
        self.creature = creature

    # Viewer does not modify thought
    def step(self, thought, world, heart, memory):
        return []

    # Called when a force packet arrives
    def handle_force_packet(self, packet):
        forces = packet.get("data", {})

        print("=== 💥 FORCE REPORT ===")

        if not forces:
            print("(no forces)")
            print("======================")
            return

        # Pretty-print each force
        for name, value in forces.items():
            print(f"{name:20} {value:+.4f}")

        print("======================")
