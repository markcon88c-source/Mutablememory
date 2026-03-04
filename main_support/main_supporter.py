# ============================================================
#  MAIN SUPPORTER – v2.0
#  Central wiring harness for the entire creature
#  Handles:
#    • MathBlock flow
#    • Force updates
#    • Story metrics
#    • World updates
#    • Cognition updates
#    • Birth force updates
#    • Flow reset (for Wiring Viewer)
# ============================================================

class MainSupporter:

    def __init__(self, creature):
        self.c = creature

    # --------------------------------------------------------
    # 1. MATH BLOCK FLOW
    # --------------------------------------------------------
    def wire_mathblocks(self):
        """
        Push every math block through the MathBlockForceCore.
        This is the circulatory system of the creature.
        """
        for block in self.c.mathblocks.blocks.values():
            self.c.mathblock_force_core.update(
                block,
                identity=self.c.name_heart,
                memory=self.c.stm,
                world=self.c.world
            )

    # --------------------------------------------------------
    # 2. STORY METRICS
    # --------------------------------------------------------
    def wire_story_metrics(self):
        """
        Story metrics depend on the full system snapshot.
        """
        try:
            snapshot = self.c.integrator.snapshot()
            self.c.story_metrics.update_from_snapshot(snapshot)
        except Exception:
            pass

    # --------------------------------------------------------
    # 3. WORLD
    # --------------------------------------------------------
    def wire_world(self):
        """
        World organs update based on the global snapshot.
        """
        try:
            snapshot = self.c.integrator.snapshot()
            self.c.world.update_from_snapshot(snapshot)
        except Exception:
            pass

    # --------------------------------------------------------
    # 4. COGNITION (STM + L-Levels)
    # --------------------------------------------------------
    def wire_cognition(self):
        """
        STM and L-Levels evolve based on the system snapshot.
        """
        try:
            snapshot = self.c.integrator.snapshot()
            self.c.stm.update_from_snapshot(snapshot)
            self.c.l_levels.update_from_snapshot(snapshot)
        except Exception:
            pass

    # --------------------------------------------------------
    # 5. BIRTH FORCES
    # --------------------------------------------------------
    def wire_birth_forces(self):
        """
        Birth forces evolve based on the global snapshot.
        """
        try:
            snapshot = self.c.integrator.snapshot()
            self.c.birth_forces.update_from_snapshot(snapshot)
        except Exception:
            pass

    # --------------------------------------------------------
    # 6. RESET FLOW FLAGS
    # --------------------------------------------------------
    def reset_flow(self):
        """
        Reset math block flow flags so ON/OFF is per heartbeat.
        """
        try:
            self.c.mathblock_force_core.reset_flow_flags(
                self.c.mathblocks.blocks
            )
        except Exception:
            pass

    # --------------------------------------------------------
    # 7. MASTER WIRING CALL
    # --------------------------------------------------------
    def wire_everything(self):
        """
        Called once per heartbeat.
        This is the creature's nervous system.
        """
        self.wire_mathblocks()
        self.wire_story_metrics()
        self.wire_world()
        self.wire_cognition()
        self.wire_birth_forces()
        self.reset_flow()
