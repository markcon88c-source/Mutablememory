# command_report_viewer.py
# ============================================================
# HYBRID COMMAND REPORT VIEWER
# Scans all successfully loaded organs and prints callable
# methods as "commands". Works with the quiet auto-loader.
# ============================================================

import inspect
from creature import Creature


class CommandReportViewer:
    def __init__(self, creature):
        self.creature = creature

    def is_command_method(self, name, value):
        # Skip private/dunder methods
        if name.startswith("_"):
            return False
        if not callable(value):
            return False
        return True

    def run(self):
        print("\n=== COMMAND REPORT VIEWER ===\n")

        organs = getattr(self.creature, "organs", [])

        for ow in organs:
            organ_name = getattr(ow, "name", "<noname>")
            organ = getattr(ow, "organ", None)
            if organ is None:
                continue

            print(f"[Organ] {organ_name} -> {organ.__class__.__name__}")

            members = inspect.getmembers(organ)
            commands_found = False

            for name, value in members:
                if self.is_command_method(name, value):
                    commands_found = True
                    print(f"  - {name}()")

            if not commands_found:
                print("  (no commands detected)")

            print()

        print("=== END OF REPORT ===\n")


if __name__ == "__main__":
    creature = Creature()
    viewer = CommandReportViewer(creature)
    viewer.run()
