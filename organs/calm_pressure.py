from organs.base_organ import BaseOrgan

class CalmPressure(BaseOrgan):
    """
    Cathedral CalmPressure
    Works with PressureCore instead of replacing it.
    Boosts calm, reduces alert, and encourages curiosity.
    """

    def __init__(self, creature):
        super().__init__(creature)
        self.calm = 0.0
        self.curiosity = 0.0

    def step(self):
        core = self.creature.organs.get("PressureCore")
        if not core:
            return {}

        p = core.get_pressures()

        storm = p["storm"]
        alert = p["alert"]
        symbolic = p["symbolic"]
        echo = core.echo
        drift = core.drift

        # -----------------------------------------------------
        # Calm generation (juiced)
        # -----------------------------------------------------
        # Calm grows when:
        # - echo is high (deep resonance)
        # - storm is low
        # - alert is low
        # - drift is stable
        self.calm = (
            0.4 * echo +
            0.3 * (1.0 - min(storm, 1.0)) +
            0.2 * (1.0 - min(alert, 1.0)) +
            0.1 * (1.0 - abs(drift))
        )

        # -----------------------------------------------------
        # Curiosity generation (juiced)
        # -----------------------------------------------------
        # Curiosity grows when:
        # - symbolic pressure is high
        # - alert is low
        # - storm is moderate (not zero)
        self.curiosity = max(
            0.0,
            symbolic * 0.5 - alert * 0.2 + 0.2 * (1.0 - abs(storm - 0.5))
        )

        # -----------------------------------------------------
        # Feed calm + curiosity back into PressureCore
        # -----------------------------------------------------
        # Calm deepens echo and stabilizes drift
        core.echo *= (1.0 + 0.1 * self.calm)
        core.drift *= (1.0 - 0.05 * self.calm)

        # Curiosity boosts spark and symbolic resonance
        core.spark *= (1.0 + 0.05 * self.curiosity)
        core.pressures["symbolic"] *= (1.0 + 0.1 * self.curiosity)

        return {
            "calm": self.calm,
            "curiosity": self.curiosity,
        }
