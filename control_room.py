# control_room.py

class ControlRoomOrgan:
    def __init__(self):
        self.drift_floor = 0.20
        self.drift_ceiling = 0.80
        self.pressure_floor = 0.15
        self.pressure_ceiling = 0.85
        self.cluster_threshold = 0.15

    # ------------------------------------------------------------
    # PRESSURE REGULATION
    # ------------------------------------------------------------
    def adjust_pressure(self, value):
        if value < self.pressure_floor:
            value = value + 0.03
        elif value > self.pressure_ceiling:
            value = value - 0.03

        if value < 0.0:
            value = 0.0
        if value > 1.0:
            value = 1.0

        return value

    def enforce_pressure_diversity(self, pressures):
        symbolic = pressures["symbolic"]
        calm = pressures["calm"]
        concentration = pressures["concentration"]
        word_strength = pressures["word_strength"]

        values = [
            symbolic,
            calm,
            concentration,
            word_strength
        ]

        max_v = max(values)
        min_v = min(values)
        spread = max_v - min_v

        if spread < self.cluster_threshold:
            pressures["symbolic"] = symbolic - 0.02
            pressures["calm"] = calm + 0.02
            pressures["concentration"] = concentration - 0.02
            pressures["word_strength"] = word_strength + 0.02

        for key in pressures:
            v = pressures[key]
            if v < 0.0:
                v = 0.0
            if v > 1.0:
                v = 1.0
            pressures[key] = v

        return pressures

    # ------------------------------------------------------------
    # BREAKOUT PROTOCOL
    # ------------------------------------------------------------
    def breakout_protocol(self, pressures):
        symbolic = pressures["symbolic"]
        calm = pressures["calm"]
        concentration = pressures["concentration"]
        word_strength = pressures["word_strength"]
        storm = pressures["storm"]
        alert = pressures["alert"]

        if (
            symbolic > 0.90 and
            calm > 0.90 and
            concentration > 0.90 and
            word_strength > 0.90 and
            storm < 0.10 and
            alert < 0.10
        ):
            pressures["symbolic"] = symbolic - 0.20
            pressures["calm"] = calm - 0.20
            pressures["concentration"] = concentration - 0.10
            pressures["word_strength"] = word_strength - 0.10

            pressures["storm"] = storm + 0.20
            pressures["alert"] = alert + 0.20

        for key in pressures:
            v = pressures[key]
            if v < 0.0:
                v = 0.0
            if v > 1.0:
                v = 1.0
            pressures[key] = v

        return pressures

    # ------------------------------------------------------------
    # STORM-DRIVEN PRESSURE SHIFT (THE HEARTBEAT)
    # ------------------------------------------------------------
    def storm_shift(self, pressures):
        storm = pressures["storm"]

        # High storm shakes the system
        if storm > 0.40:
            pressures["alert"] = pressures["alert"] + 0.05
            pressures["symbolic"] = pressures["symbolic"] + 0.03
            pressures["word_strength"] = pressures["word_strength"] + 0.03
            pressures["calm"] = pressures["calm"] - 0.04
            pressures["concentration"] = pressures["concentration"] - 0.04

        # Low storm settles the system
        elif storm < 0.20:
            pressures["calm"] = pressures["calm"] + 0.04
            pressures["concentration"] = pressures["concentration"] + 0.04
            pressures["alert"] = pressures["alert"] - 0.03
            pressures["symbolic"] = pressures["symbolic"] - 0.02

        # Clamp
        for key in pressures:
            v = pressures[key]
            if v < 0.0:
                v = 0.0
            if v > 1.0:
                v = 1.0
            pressures[key] = v

        return pressures

    # ------------------------------------------------------------
    # DRIFT-LINKED INSTABILITY INJECTION
    # ------------------------------------------------------------
    def inject_instability(self, pressures, drift):
        intensity = drift["intensity"]

        if intensity < 0.10:
            pressures["storm"] = pressures["storm"] + 0.05
            pressures["alert"] = pressures["alert"] + 0.05

        for key in pressures:
            v = pressures[key]
            if v < 0.0:
                v = 0.0
            if v > 1.0:
                v = 1.0
            pressures[key] = v

        return pressures

    # ------------------------------------------------------------
    # DRIFT REGULATION
    # ------------------------------------------------------------
    def adjust_drift(self, drift):
        intensity = drift["intensity"]

        if intensity < self.drift_floor:
            intensity = intensity + 0.03
        elif intensity > self.drift_ceiling:
            intensity = intensity - 0.03

        if intensity < 0.0:
            intensity = 0.0
        if intensity > 1.0:
            intensity = 1.0

        drift["intensity"] = round(intensity, 2)
        return drift

    # ------------------------------------------------------------
    # WORLD RECURSION PREVENTION
    # ------------------------------------------------------------
    def adjust_world_balance(self, state):
        thought = state["thought"]
        world = state["world"]

        if thought == world:
            state["world"] = world + " field"

        return state

    # ------------------------------------------------------------
    # MASTER ADJUST
    # ------------------------------------------------------------
    def adjust(self, state):
        # 1. Pressure regulation
        for key in state["pressures"]:
            v = state["pressures"][key]
            state["pressures"][key] = self.adjust_pressure(v)

        # 2. Pressure diversity
        state["pressures"] = self.enforce_pressure_diversity(
            state["pressures"]
        )

        # 3. Breakout protocol
        state["pressures"] = self.breakout_protocol(
            state["pressures"]
        )

        # 4. Storm-driven pressure shift
        state["pressures"] = self.storm_shift(
            state["pressures"]
        )

        # 5. Drift-linked instability injection
        state["pressures"] = self.inject_instability(
            state["pressures"],
            state["drift"]
        )

        # 6. Drift regulation
        state["drift"] = self.adjust_drift(
            state["drift"]
        )

        # 7. World recursion prevention
        state = self.adjust_world_balance(state)

        return state




