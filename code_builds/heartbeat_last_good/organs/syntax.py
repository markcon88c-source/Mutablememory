import random


class SyntaxOrgan:
    def __init__(self):
        self.stm = {
            "last_syntax": None
        }

    def compute_pressures(self, mood_state, drift, sym_p, alert_p):
        calm = mood_state.get("calm", 0.0)
        curious = mood_state.get("curious", 0.0)
        bright = mood_state.get("bright", 0.0)

        syntax_pressure = (
            (curious * 0.4) +
            (bright * 0.3) +
            (sym_p * 0.3)
        )

        stability_pressure = (
            (calm * 0.5) +
            (1.0 - alert_p) * 0.
