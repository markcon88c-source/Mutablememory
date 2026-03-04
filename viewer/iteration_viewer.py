class IterationViewer:
    def __init__(self, creature):
        self.creature = creature
        self.iteration = 0

    def view(self):
        # Pull state from organs
        lang = self.creature.language_organ
        brush = self.creature.brushup_organ

        asc_state = getattr(lang, "ascension_state", None)
        brushups = getattr(brush, "cycle", 0)

        # Emoji mapping for ascension
        asc_emoji = {
            None: "⚪",
            "seed": "🌱",
            "sprout": "🌿",
            "tree": "🌳⚡",
            "ascended": "💎💚"
        }.get(asc_state, "❓")

        # Brushup bar (4 required)
        brush_bar = (
            "🟩" * min(brushups, 4) +
            "⬜" * max(0, 4 - brushups)
        )

        # Activation condition
        ready = asc_state == "ascended" and brushups >= 4

        if ready:
            self.iteration += 1
            return {
                "viewer": "IterationViewer",
                "status": "iteration_active",
                "iteration": self.iteration,
                "iteration_emoji": f"🔁{self.iteration}",
                "ascension_state": asc_state,
                "ascension_emoji": asc_emoji,
                "brushups": brushups,
                "brushup_bar": brush_bar,
                "activation": "💎✨ Brushups complete — iteration unlocked!"
            }

        # Waiting state
        return {
            "viewer": "IterationViewer",
            "status": "waiting_for_conditions",
            "iteration": self.iteration,
            "ascension_state": asc_state,
            "ascension_emoji": asc_emoji,
            "brushups": brushups,
            "brushup_bar": brush_bar,
            "activation": "⏳ Waiting for Emerald + 4 Brushups"
        }
