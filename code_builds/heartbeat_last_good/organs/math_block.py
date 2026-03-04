from decimal import Decimal, getcontext

# High precision for meaning math
getcontext().prec = 24


class MathBlock:
    """
    Generates exact, nonlinear target values for each level.
    The STMOrgan treats these as sacred gate numbers.
    """

    def __init__(self):
        # You can later tune this or make it depend on pressure, mood, etc.
        self.base_start = Decimal("0.40")
        self.base_step = Decimal("0.06")
        self.micro_mod = Decimal("0.013579")

    def target_for_level(self, level: int) -> Decimal:
        """
        Return the exact meaning value required to move from this level
        to the next. Nonlinear, level-dependent, and precise.
        """
        # Base progression
        base = self.base_start + Decimal(level - 1) * self.base_step

        # Nonlinear tweak: wraps inside a small band to avoid linearity
        tweak = (Decimal(level) * self.micro_mod) % Decimal("0.010000000000000")

        target = base + tweak
        return target.quantize(Decimal("0.000000000000001"))
