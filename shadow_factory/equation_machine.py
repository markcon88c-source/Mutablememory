import random

class ShadowEquationMachine:
    def __init__(self):
        self.equation_buffer = []
        self.complexity_on = False   # status flag

    def set_complexity_state(self, state):
        self.complexity_on = state

    def add_equation(self, eq):
        self.equation_buffer.append(eq)

    def generate_equation(self):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        eq = f"{a}x^2 + {b}x + {c} = 0"
        self.equation_buffer.append(eq)

    def heartbeat_output(self):
        print("shadow-equation-heartbeat")
        print(f"[complexity: {'ON' if self.complexity_on else 'OFF'}]")

        self.generate_equation()

        if len(self.equation_buffer) > 0:
            sample_size = min(5, len(self.equation_buffer))
            sample = random.sample(self.equation_buffer, sample_size)

            print("\n--- sample ---")
            for eq in sample:
                print(eq)
            print("--------------\n")
