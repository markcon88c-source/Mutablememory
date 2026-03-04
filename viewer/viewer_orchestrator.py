# ============================================================
# VIEWER ORCHESTRATOR — Cathedral Viewer Spine
# ============================================================

class ViewerOrchestrator:
    def __init__(self, creature, governor, translator):
        self.creature = creature
        self.governor = governor
        self.translator = translator

    def render(self, packet):
        # Choose viewer
        viewer = self.governor.choose_viewer()
        if viewer is None:
            return

        # Translate packet
        translated = self.translator.translate(packet)

        # Render viewer output
        try:
            output = viewer.render(translated)
        except Exception as e:
            output = [f"[Viewer Error: {e}]"]

        # Normalize to list
        if isinstance(output, str):
            output = output.split("\n")

        # Clear frame spacing
        print("\n" * 2)
        print("============================================================")
        print(f"=== {viewer.__class__.__name__.upper()} ===")
        print("============================================================")

        # Print only this viewer
        for line in output:
            print(line)
