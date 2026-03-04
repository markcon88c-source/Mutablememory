class SolverMachine:
    def __init__(self):
        self.equation_memory = []
        self.rules = []
        self.gremlin_rule = None
        self.default_value = 1

    def set_gremlin_rule(self, rule_fn):
        """Assign the gremlin override rule."""
        self.gremlin_rule = rule_fn

    def add_rule(self, rule_fn):
        """Add normal solver rules."""
        self.rules.append(rule_fn)

    def remember(self, equation):
        self.equation_memory.append(equation)

    def solve_math_block(self, math_block, interpretation_block):
        print("SOLVER MACHINE:")
        print("  Received math block:", math_block)
        print("  Assigned to equation:", interpretation_block)

        # -------------------------
        # 1. GREMLIN OVERRIDE
        # -------------------------
        if self.gremlin_rule:
            gremlin_solution, gremlin_ok = self.gremlin_rule(
                math_block, interpretation_block
            )
            if gremlin_ok:
                print("  Gremlin override activated:", gremlin_solution)
                return gremlin_solution

        # -------------------------
        # 2. NORMAL RULE PIPELINE
        # -------------------------
        self.remember(interpretation_block)

        for rule in self.rules:
            solution, ok = rule(interpretation_block)
            if ok:
                print("  Solver succeeded:", solution)
                return solution

        # -------------------------
        # 3. FALLBACK
        # -------------------------
        fallback = {"fallback": self.default_value}
        print("  Solver defaulted:", fallback)
        return fallback
