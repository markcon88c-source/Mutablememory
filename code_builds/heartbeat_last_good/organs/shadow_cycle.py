from shadow_factory.equation_machine import ShadowEquationMachine

class ShadowCycle:
    def __init__(self, heart):
        self.heart = heart
        self.eq_machine = ShadowEquationMachine()

    def run(self):
        tick = self.heart.run()
        if tick is None:
            return

        # Trigger the shadow equation machine
        self.eq_machine.heartbeat_output()
from shadow_factory.equation_machine import ShadowEquationMachine
from shadow_factory.math_complexity_machine import ShadowMathComplexityMachine

class ShadowCycle:
    def __init__(self, heart):
        self.heart = heart
        self.eq_machine = ShadowEquationMachine()
        self.complex_machine = ShadowMathComplexityMachine(self.eq_machine)

    def run(self):
        tick = self.heart.run()
        self.eq_machine.set_complexity_state(self.complex_machine.on)
        if tick is None:
            return

        # first generate complex math
        self.complex_machine.heartbeat_output()

        # then display it
        self.eq_machine.heartbeat_output()
