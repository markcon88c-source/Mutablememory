# MATH BLOCK VIEWER — shows what ascension tier the math block is attacking toward

class MathBlockViewer:
    def __init__(self):
        self.expression = None
        self.value = None
        self.tokens = []
        self.force = 0.0
        self.attack = "none"      # "up", "down", "hold"
        self.ascension = 0        # 0–3
        self.stability = 0        # 0–3

    def accept(self, packet):
        if packet.get("type") == "math_block":
            payload = packet.get("payload", {})

            # Expecting:
            # {
            #   "expression": "...",
            #   "value": number or None,
            #   "tokens": [...],
            #   "force": 0.0–1.0,
            #   "attack": "up/down/hold",
            #   "ascension": 0–3,
            #   "stability": 0–3
            # }
            self.expression = payload.get("expression", self.expression)
            self.value = payload.get("value", self.value)
            self.tokens = payload.get("tokens", self.tokens)
            self.force = payload.get("force", self.force)
            self.attack = payload.get("attack", self.attack)
            self.ascension = payload.get("ascension", self.ascension)
            self.stability = payload.get("stability", self.stability)

    def render(self):
        if self.expression is None:
            return "[MathBlockViewer] …awaiting math block…"

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

        # Attack vector arrow
        if self.attack == "up":
            arrow = "↑"
        elif self.attack == "down":
            arrow = "↓"
        else:
            arrow = "→"

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

        force_bar = bar(self.force)

        # Token string
        token_str = " ".join(str(t) for t in self.tokens) if self.tokens else "(none)"

        return (
            f"[MathBlockViewer {icon}] Math block ascension attack\n"
            f"Ascension: {asc_symbol}\n"
            f"Attack: {arrow} ({self.attack})\n"
            f"Force: {force_bar} ({self.force:.2f})\n"
            f"Expression: {self.expression}\n"
            f"Value: {self.value}\n"
            f"Tokens: {token_str}"
        )
