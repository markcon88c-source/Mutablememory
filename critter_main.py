from organs.five_stack_registry import FiveStackOrganRegistry
from critter.viewer.five_stack_viewer_registry import FiveStackViewerRegistry


class Creature:
    def __init__(self):
        # Load all organs and viewers
        self.organ_registry = FiveStackOrganRegistry()
        self.viewer_registry = FiveStackViewerRegistry()

        self.organs = self.organ_registry.load_all(self)
        self.viewers = self.viewer_registry.load_all(self)

        self.iteration = 0

    def heartbeat(self):
        """
        Full unified heartbeat:
        1. Build base packet
        2. Run all organs (metabolism)
        3. Run all viewers (expression)
        4. Merge outputs cleanly
        5. Return final packet
        """

        # Base packet
        packet = {"router": {"iteration": self.iteration}}

        # ----------------------------------------------------
        # 1. ORGANS — metabolism, pressure, routing, sentence
        # ----------------------------------------------------
        organ_outputs = {}
        for organ in self.organs:
            try:
                out = organ.tick(self.iteration, packet)
                if out:
                    organ_outputs.update(out)
            except Exception as e:
                organ_outputs[f"error_{organ.__class__.__name__}"] = str(e)

        packet.update(organ_outputs)

        # ----------------------------------------------------
        # 2. VIEWERS — language, narrative, brush-up, emergence
        # ----------------------------------------------------
        viewer_outputs = {}
        for viewer in self.viewers:
            try:
                out = viewer.render(packet)
                if out:
                    viewer_outputs.update(out)
            except Exception as e:
                viewer_outputs[f"error_{viewer.__class__.__name__}"] = str(e)

        packet.update(viewer_outputs)

        # ----------------------------------------------------
        # 3. Increment iteration + return final packet
        # ----------------------------------------------------
        self.iteration += 1
        return packet
