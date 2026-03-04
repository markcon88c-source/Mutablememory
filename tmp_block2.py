# =========================================================
# tmp_block2.py — Critter Core Cycle (Block 2)
# =========================================================

    # -----------------------------------------------------
    # Core cycle — one heartbeat
    # -----------------------------------------------------
    def step(self):
        self.tick += 1

        # -----------------------------
        # DRIFT
        # -----------------------------
        drift_state = {
            "intensity": self.storm.intensity(self.tick),
            "tone": self.storm.tone(self.tick)
        }

        # -----------------------------
        # MOOD
        # -----------------------------
        mood_state = self.mood.generate(drift_state)

        # -----------------------------
        # RAW PRESSURES
        # -----------------------------
        raw_pressures = {
            "alert": self.alert.compute(mood_state, drift_state),
            "calm": self.calm.compute(mood_state, drift_state),
            "concentration": self.concentration.compute(mood_state, drift_state),
            "symbolic": self.symbolic.compute(mood_state, drift_state),
            "word_strength": self.word_strength.compute(mood_state, drift_state)
        }

        # -----------------------------
        # CONTROL ROOM — corrected pressures
        # -----------------------------
        corrected = self.control_room.balance(raw_pressures, drift_state)

        # -----------------------------
        # THOUGHT
        # -----------------------------
        thought_output = self.thought.generate({
            "mood": mood_state,
            "drift": drift_state,
            "pressures": corrected
        })

        # -----------------------------
        # VERB
        # -----------------------------
        verb_output = self.verb.generate({
            "mood": mood_state,
            "drift": drift_state,
            "pressures": corrected,
            "thought": thought_output
        })

        # -----------------------------
        # REACTION
        # -----------------------------
        reaction_output = self.reaction.generate({
            "mood": mood_state,
            "drift": drift_state,
            "pressures": corrected,
            "thought": thought_output,
            "verb": verb_output
        })

        # -----------------------------
        # WORLD
        # -----------------------------
        world_output = self.world.generate({
            "mood": mood_state,
            "drift": drift_state,
            "pressures": corrected,
            "thought": thought_output,
            "verb": verb_output,
            "reaction": reaction_output
        })

        # -----------------------------
        # REALITY
        # -----------------------------
        real_output = self.real.generate({
            "mood": mood_state,
            "drift": drift_state,
            "pressures": corrected
        })
