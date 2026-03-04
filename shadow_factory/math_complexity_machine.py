import random

class ShadowMathComplexityMachine:
    def __init__(self, eq_machine):
        self.eq_machine = eq_machine
        self.on = False   # complexity OFF by default

    def turn_on(self):
        self.on = True

    def turn_off(self):
        self.on = False

    def generate_complex_equation(self):
        # placeholder complexity — will evolve later
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        d = random.randint(1, 9)

        eq = f"({a}x + {b})({c}x + {d}) = 0"
        return eq

    def heartbeat_output(self):
        if not self.on:
            return  # complexity disabled

        eq = self.generate_complex_equation()
        self.eq_machine.add_equation(eq)
