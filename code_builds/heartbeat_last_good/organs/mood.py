import random

class MoodOrgan:
    """
    Handles creature mood with:
      - mood index
      - mood inertia
      - mood vector
      - mood transitions
    """

    def __init__(self):
        self.moods = [
            "calm",
            "focused",
            "curious",
            "bright",
            "chaotic"
        ]

        self.mood_vectors = {
            "calm":     {"calm": 1.0, "alert": 0.1},
            "focused":  {"calm": 0.6, "alert": 0.6},
            "curious":  {"calm": 0.4, "alert": 0.8},
            "bright":   {"calm": 0.2, "alert": 1.0},
            "chaotic":  {"calm": 0.1, "alert": 1.2}
        }

        self.current_index = 0
        self.inertia = 0.85

    def choose_next(self):
        """
        Choose next mood with inertia.
        """
        r = random.random()

        if r < self.inertia:
            return self.current_index

        shift = random.choice([-1, 1])
        nxt = self.current_index + shift

        if nxt < 0:
            nxt = 0
        if nxt >= len(self.moods):
            nxt = len(self.moods) - 1

        return nxt

    def update(self):
        """
        Update mood for this cycle.
        Returns:
          - mood_name
          - mood_vector
        """
        nxt = self.choose_next()
        self.current_index = nxt

        name = self.moods[nxt]
        vec = self.mood_vectors.get(name, {"calm": 0.5, "alert": 0.5})

        return name, vec

    def packet(self, name, vec):
        """
        Return a mood packet for the viewer or state.
        """
        return {
            "mood_name": name,
            "mood_vector": dict(vec)
        }

    # ---------------------------------------------------------
    # NEW METHOD — required by main.py
    # ---------------------------------------------------------
    def generate(self, pressure_state):
        """
        Adapter for main.py.
        Calls update() and returns a mood packet.
        """
        name, vec = self.update()
        return {
            "mood": name,
            "vector": vec,
            "valence": vec.get("calm", 0.5),
            "arousal": vec.get("alert", 0.5),
            "stability": 1.0 - abs(vec.get("alert", 0.5) - vec.get("calm", 0.5))
        }
