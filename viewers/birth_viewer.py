# BIRTH VIEWER — party atmosphere when a character is born

class BirthViewer:
    def __init__(self):
        self.name = None
        self.seed = None
        self.role = None
        self.forces = {}
        self.ascension = 0
        self.stability = 0
        self.seen_birth = False

    def accept(self, packet):
        ptype = packet.get("type")

        # Birth packet — the party starts here
        if ptype == "character_birth":
            payload = packet["payload"]
            self.name = payload.get("name")
            self.seed = payload.get("seed")
            self.seen_birth = True

        # Sheet packet — role arrives shortly after birth
        elif ptype == "character_sheet":
            payload = packet["payload"]
            self.role = payload.get("role")

        # Forces packet — newborn touched lightly
        elif ptype == "character_forces":
            self.forces = packet.get("payload", {})

        # Identity packet — ascension + stability
        elif ptype == "identity":
            ident = packet.get("payload", {})
            self.ascension = ident.get("ascension", self.ascension)
            self.stability = ident.get("stability", self.stability)

    def render(self):
        if not self.seen_birth:
            return "[BirthViewer] …awaiting birth…"

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

        # Party sparkles (Termux‑safe)
        party = "✨🎉✨" if self.ascension >= 2 else "✨"

        # Light force influence
        force_lines = []
        for k, v in self.forces.items():
            if v > 0.15:
                mark = "*"
            elif v > 0.05:
                mark = "·"
            else:
                mark = " "
            force_lines.append(f"{k:10} | {mark}")

        forces_block = "\n".join(force_lines) if force_lines else "none"

        return (
            f"[BirthViewer {icon}] {party} A character is born! {party}\n"
            f"Name: {self.name}\n"
            f"Seed: {self.seed}\n"
            f"Role: {self.role}\n"
            f"Ascension: {asc_symbol}\n"
            f"Forces touching the newborn:\n{forces_block}"
        )
