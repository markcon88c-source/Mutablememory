class WordStrengthUpdate:
    def update(self, state):
        strengths = state.get("word_strengths", {})
        pressure = state["pressures"].get("word_strength", 0.0)
        blocks = state.get("math_blocks", {})

        updated = {}

        for word, value in strengths.items():
            block = blocks.get(word, {})
            block_bias = block.get("pressure_bias", 0.0)

            # 15-decimal developmental micro-adjustment
            delta = (pressure * 0.000000000000010)
            delta += block_bias * 0.000000000000005

            new_value = value + delta

            # Safety clamp
            if new_value < 0.0:
                new_value = 0.0

            updated[word] = new_value

        state["word_strengths"] = updated
        return state
