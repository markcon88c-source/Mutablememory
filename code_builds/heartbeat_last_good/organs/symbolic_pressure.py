# symbolic_pressure.py

class SymbolicPressure:
    def compute(self, state):
        current = state["pressures"]["symbolic"]
        p = state["pressures"]
        mood = state["mood"]

        target = (
            0.4 * p["storm"] +
            0.3 * p["alert"] +
            0.3 * mood["valence"]
        )

        gain = 0.10 + 0.20 * mood["arousal"]

        new = current + (target - current) * gain
        return max(0.0, min(1.0, round(new, 2)))