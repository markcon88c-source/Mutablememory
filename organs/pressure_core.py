import math
import random

class PressureCore:
    """
    Cathedral PressureCore

    Force ecology for:
      - primal forces: spark, drift, echo
      - storm mechanics: intensity, coherence, direction
      - seven pressures:
          storm, calm, symbolic, alert,
          concentration, word_strength, memory

    This is a rule-rich, hybrid system:
      - additive rules
      - multiplicative rules
      - thresholds
      - resonance
      - collisions
      - decay
      - feedback
      - circadian + mood modulation
    """

    def __init__(self, creature):
        self.creature = creature

        # primal forces
        self.spark = 0.0
        self.drift = 0.0
        self.echo = 0.0

        # storm state
        self.storm = {
            "intensity": 0.0,
            "coherence": 0.0,
            "direction": 0.0,  # -1..1
        }

        # seven pressures
        self.pressures = {
            "storm": 0.0,
            "calm": 0.0,
            "symbolic": 0.0,
            "alert": 0.0,
            "concentration": 0.0,
            "word_strength": 0.0,
            "memory": 0.0,
        }

        # memory of past storms / echoes
        self.storm_history = []
        self.echo_history = []

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def step(self, inputs=None):
        """
        Main metabolic tick.
        `inputs` can optionally bias primal forces:
          {
            "spark_bias": float,
            "drift_bias": float,
            "echo_bias": float
          }
        """
        if inputs is None:
            inputs = {}

        self.update_primal(inputs)
        self.apply_interactions()
        self.update_storm()
        self.emit_pressures()
        self.apply_feedback()
        self.apply_circadian_modulation()
        self.apply_mood_modulation()
        self.update_memory_pressure()

        return dict(self.pressures)

    def get_pressures(self):
        return dict(self.pressures)

    # ---------------------------------------------------------
    # Layer 1 — primal force update
    # ---------------------------------------------------------
    def update_primal(self, inputs):
        # base noise to keep system alive
        noise_spark = random.uniform(-0.05, 0.1)
        noise_drift = random.uniform(-0.05, 0.05)
        noise_echo = random.uniform(-0.02, 0.08)

        spark_bias = inputs.get("spark_bias", 0.0)
        drift_bias = inputs.get("drift_bias", 0.0)
        echo_bias = inputs.get("echo_bias", 0.0)

        # simple bounded update
        self.spark = self._clamp(self.spark + 0.3 * spark_bias + noise_spark, 0.0, 1.5)
        self.drift = self._clamp(self.drift + 0.2 * drift_bias + noise_drift, -1.0, 1.0)
        self.echo = self._clamp(self.echo + 0.25 * echo_bias + noise_echo, 0.0, 1.5)

    # ---------------------------------------------------------
    # Layer 2 — interaction lattice (many rules)
    # ---------------------------------------------------------
    def apply_interactions(self):
        s = self.spark
        d = abs(self.drift)
        e = self.echo

        # --- additive rules ---
        # spark feeds storm
        self.pressures["storm"] += 0.4 * s
        # echo feeds calm
        self.pressures["calm"] += 0.3 * e
        # drift feeds concentration
        self.pressures["concentration"] += 0.25 * d

        # --- multiplicative rules ---
        # spark × drift → storm amplification
        self.pressures["storm"] += 0.6 * s * d
        # echo × echo → deep calm
        self.pressures["calm"] += 0.5 * (e ** 2)
        # drift × echo → symbolic
        self.pressures["symbolic"] += 0.5 * d * e

        # --- threshold rules ---
        if s > 0.7 and d > 0.4:
            self.pressures["storm"] += 0.5
        if e > 0.8 and self.pressures["storm"] < 0.3:
            self.pressures["calm"] += 0.4
        if self.pressures["symbolic"] > 0.6:
            self.pressures["word_strength"] += 0.3

        # --- resonance rules ---
        # oscillation-like behavior: spark vs echo
        resonance = abs(s - e)
        if resonance < 0.2:
            # in-phase → symbolic resonance
            self.pressures["symbolic"] += 0.4
        else:
            # out-of-phase → alertness
            self.pressures["alert"] += 0.3

        # drift stability → storm coherence
        if d > 0.6:
            self.storm["coherence"] = self._clamp(self.storm["coherence"] + 0.2, 0.0, 1.0)
        else:
            self.storm["coherence"] *= 0.9

        # --- collision rules ---
        # spark vs echo → symbolic tension
        self.pressures["symbolic"] += 0.2 * abs(s - e)

        # opposing drift directions over time → calm
        if len(self.storm_history) >= 1:
            last_dir = self.storm_history[-1]["direction"]
            if last_dir * self.drift < -0.3:
                self.pressures["calm"] += 0.3

        # storm vs calm → memory
        self.pressures["memory"] += 0.2 * abs(self.pressures["storm"] - self.pressures["calm"])

        # --- decay rules (local) ---
        # keep pressures bounded and slightly decaying
        for k in self.pressures:
            self.pressures[k] *= 0.9

    # ---------------------------------------------------------
    # Layer 3 — storm mechanics
    # ---------------------------------------------------------
    def update_storm(self):
        s = self.spark
        d = self.drift
        e = self.echo

        # base storm intensity from spark + drift
        base_intensity = 0.5 * s + 0.4 * abs(d)

        # echo can either deepen or dampen storms
        if e < 0.5:
            base_intensity *= (1.0 + 0.3 * e)
        else:
            base_intensity *= (1.0 - 0.2 * (e - 0.5))

        # threshold for storm formation
        if base_intensity > 0.6:
            self.storm["intensity"] = self._clamp(
                self.storm["intensity"] + 0.3 * base_intensity, 0.0, 2.0
            )
        else:
            # decay
            self.storm["intensity"] *= 0.85

        # direction follows drift with some noise
        self.storm["direction"] = self._clamp(
            0.7 * self.storm["direction"] + 0.3 * d + random.uniform(-0.05, 0.05),
            -1.0,
            1.0,
        )

        # coherence grows with stable direction and echo
        if abs(self.storm["direction"]) > 0.4 and e > 0.4:
            self.storm["coherence"] = self._clamp(
                self.storm["coherence"] + 0.1 * e, 0.0, 1.0
            )
        else:
            self.storm["coherence"] *= 0.9

        # record storm history for collision rules
        self.storm_history.append(
            {
                "intensity": self.storm["intensity"],
                "direction": self.storm["direction"],
                "coherence": self.storm["coherence"],
            }
        )
        if len(self.storm_history) > 50:
            self.storm_history.pop(0)

    # ---------------------------------------------------------
    # Layer 4 — pressure emission
    # ---------------------------------------------------------
    def emit_pressures(self):
        intensity = self.storm["intensity"]
        coherence = self.storm["coherence"]

        # storm pressure from intensity + coherence
        self.pressures["storm"] += 0.7 * intensity + 0.4 * coherence

        # calm pressure from echo and low storm
        self.pressures["calm"] += 0.5 * self.echo * (1.0 - min(intensity, 1.0))

        # symbolic pressure from echo + coherence
        self.pressures["symbolic"] += 0.4 * self.echo * coherence

        # alert pressure from rapid changes in storm
        if len(self.storm_history) >= 2:
            last = self.storm_history[-2]["intensity"]
            delta = abs(intensity - last)
            self.pressures["alert"] += 0.6 * delta

        # concentration from drift stability + coherence
        self.pressures["concentration"] += 0.5 * abs(self.drift) * coherence

        # word strength from symbolic + storm
        self.pressures["word_strength"] += 0.3 * self.pressures["symbolic"] + 0.2 * intensity

        # memory pressure partly handled later, but seeded here
        self.pressures["memory"] += 0.2 * self.echo + 0.1 * intensity

    # ---------------------------------------------------------
    # Layer 5 — feedback into primal forces
    # ---------------------------------------------------------
    def apply_feedback(self):
        p = self.pressures

        # storm pressure increases spark, destabilizes drift
        self.spark = self._clamp(self.spark + 0.2 * p["storm"], 0.0, 2.0)
        self.drift = self._clamp(
            self.drift + 0.1 * p["storm"] * random.choice([-1, 1]),
            -1.0,
            1.0,
        )

        # calm pressure deepens echo, reduces spark
        self.echo = self._clamp(self.echo + 0.2 * p["calm"], 0.0, 2.0)
        self.spark = self._clamp(self.spark - 0.1 * p["calm"], 0.0, 2.0)

        # symbolic pressure stabilizes drift, boosts word strength indirectly
        self.drift = self._clamp(
            0.8 * self.drift + 0.2 * math.copysign(1.0, self.drift or 0.1),
            -1.0,
            1.0,
        )

        # alert pressure sharpens spark
        self.spark = self._clamp(self.spark + 0.15 * p["alert"], 0.0, 2.0)

        # concentration pressure narrows drift range
        self.drift = self._clamp(self.drift * (1.0 + 0.1 * p["concentration"]), -1.0, 1.0)

    # ---------------------------------------------------------
    # Layer 6 — circadian modulation
    # ---------------------------------------------------------
    def apply_circadian_modulation(self):
        state_organ = self.creature.organs.get("state_organ") if hasattr(self.creature, "organs") else None
        if not state_organ or not hasattr(state_organ, "get_circadian"):
            return

        circ = state_organ.get_circadian()
        day_intensity = circ.get("day_intensity", 0.0)
        night_intensity = circ.get("night_intensity", 0.0)

        # day: more spark, more storm, less echo
        self.spark *= (1.0 + 0.3 * day_intensity)
        self.echo *= (1.0 - 0.2 * day_intensity)

        # night: more echo, more calm, more symbolic
        self.echo *= (1.0 + 0.3 * night_intensity)
        self.pressures["calm"] *= (1.0 + 0.3 * night_intensity)
        self.pressures["symbolic"] *= (1.0 + 0.2 * night_intensity)

    # ---------------------------------------------------------
    # Layer 7 — mood modulation
    # ---------------------------------------------------------
    def apply_mood_modulation(self):
        state_organ = self.creature.organs.get("state_organ") if hasattr(self.creature, "organs") else None
        if not state_organ or not hasattr(state_organ, "_circadian"):
            return

        mood = state_organ._circadian.get("mood_index", 0.0) if isinstance(state_organ._circadian, dict) else 0.0

        # positive mood → more storm + symbolic, less alert
        if mood > 0:
            self.pressures["storm"] *= (1.0 + 0.2 * mood)
            self.pressures["symbolic"] *= (1.0 + 0.2 * mood)
            self.pressures["alert"] *= (1.0 - 0.2 * mood)
        else:
            # negative mood → more alert, more concentration
            m = abs(mood)
            self.pressures["alert"] *= (1.0 + 0.3 * m)
            self.pressures["concentration"] *= (1.0 + 0.2 * m)

    # ---------------------------------------------------------
    # Layer 8 — memory pressure
    # ---------------------------------------------------------
    def update_memory_pressure(self):
        # store echo and storm snapshots
        self.echo_history.append(self.echo)
        if len(self.echo_history) > 100:
            self.echo_history.pop(0)

        if self.storm["intensity"] > 0.7:
            self.storm_history[-1]["marked"] = True

        # memory pressure from accumulated echo + marked storms
        echo_mass = sum(self.echo_history) / max(len(self.echo_history), 1)
        marked_storms = sum(1 for s in self.storm_history if s.get("marked"))

        self.pressures["memory"] = self._clamp(
            0.5 * echo_mass + 0.2 * marked_storms,
            0.0,
            2.0,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _clamp(self, x, lo, hi):
        return lo if x < lo else hi if x > hi else x
