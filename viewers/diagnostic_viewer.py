# DIAGNOSTIC VIEWER — fun, expressive snapshot of the whole Cathedral creature

class DiagnosticViewer:
    def __init__(self):
        self.ascension = 0
        self.stability = 0

        self.forces = {}
        self.pressure = 0.0
        self.drift = 0.0
        self.identity_stage = "unknown"
        self.character_name = None
        self.ocean_clumps = 0
        self.stm_mass = 0.0
        self.math_attack = "none"

    def accept(self, packet):
        ptype = packet.get("type")
        payload = packet.get("payload", {})

        # Global ascension + stability
        if ptype == "diagnostic":
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

            self.forces = payload.get("forces", self.forces)
            self.pressure = payload.get("pressure", self.pressure)
            self.drift = payload.get("drift", self.drift)
            self.identity_stage = payload.get("identity_stage", self.identity_stage)
            self.character_name = payload.get("character_name", self.character_name)
            self.ocean_clumps = payload.get("ocean_clumps", self.ocean_clumps)
            self.stm_mass = payload.get("stm_mass", self.stm_mass)
            self.math_attack = payload.get("math_attack", self.math_attack)

    def render(self):
        # Stability → emoji
        stability_map = {
            0: "🟥",
            1: "🟨",
            2: "🟩",
            3: "💚",
        }
        icon = stability_map.get(self.stability, "🟨")

        # Ascension height
        asc_map = {
            0: "·",
            1: "─",
            2: "╱╲",
            3: "⟰",
        }
        asc_symbol = asc_map.get(self.ascension, "·")

        # Force bar
        def bar(v):
            if v > 0.75:
                return "████"
            elif v > 0.5:
                return "███"
            elif v > 0.25:
                return "██"
            elif v > 0.1:
                return "█"
            else:
                return "·"

        # Forces block
        force_lines = []
        for k, v in self.forces.items():
            force_lines.append(f"{k:10} | {bar(v)} ({v:.2f})")
        forces_block = "\n".join(force_lines) if force_lines else "none"

        # Drift arrow
        if self.drift > 0.6:
            drift_icon = "↑↑"
        elif self.drift > 0.3:
            drift_icon = "↑"
        elif self.drift > 0.1:
            drift_icon = "→"
        else:
            drift_icon = "·"

        # Math attack arrow
        if self.math_attack == "up":
            math_icon = "↑"
        elif self.math_attack == "down":
            math_icon = "↓"
        elif self.math_attack == "hold":
            math_icon = "→"
        else:
            math_icon = "·"

        return (
            f"[DiagnosticViewer {icon}] Creature diagnostic snapshot\n"
            f"Ascension: {asc_symbol}\n\n"
            f"Character: {self.character_name}\n"
            f"Identity Stage: {self.identity_stage}\n\n"
            f"Forces:\n{forces_block}\n\n"
            f"Pressure: {bar(self.pressure)} ({self.pressure:.2f})\n"
            f"Drift: {drift_icon} ({self.drift:.2f})\n\n"
            f"Ocean Clumps: {self.ocean_clumps}\n"
            f"STM Mass: {bar(self.stm_mass)} ({self.stm_mass:.2f})\n\n"
            f"Math Attack: {math_icon} ({self.math_attack})"
        )
