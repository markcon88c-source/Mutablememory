class StateOrgan:
    """
    Cathedral-era State Organ.
    Central metabolic ledger for:
      - cycle counter
      - mood index
      - circadian phase
      - returned sentences from the Shore
      - forces + pressures for MeaningOrgan
    """

    def __init__(self, creature):
        self.creature = creature
        self._returns = []          # list of return events
        self._circadian = {}        # day/night state
        self._loaded = False        # ensures load() only runs once

    # ---------------------------------------------------------
    # Load persistent state from disk
    # ---------------------------------------------------------
    def load(self):
        if self._loaded:
            return

        state = {}
        state["cycle_counter"] = load_cycle_counter()
        state["mood_index"] = load_mood_index()

        # Initialize circadian fields
        state["day_intensity"] = 0.0
        state["night_intensity"] = 0.0
        state["circadian_phase"] = 0.0
        state["is_day"] = False
        state["is_night"] = False

        # Store internally
        self._circadian = state
        self._loaded = True

    # ---------------------------------------------------------
    # Save persistent state to disk
    # ---------------------------------------------------------
    def save(self, state):
        if "cycle_counter" in state:
            save_cycle_counter(state["cycle_counter"])
        if "mood_index" in state:
            save_mood_index(state["mood_index"])

    # ---------------------------------------------------------
    # Record a returned sentence from the Shore
    # ---------------------------------------------------------
    def record_return(self, entry):
        """
        entry = {
            "sentence": str,
            "forces": {...},
            "pressures": {...},
            "score": float,
            "timestamp": str
        }
        """
        self._returns.append(entry)

    # ---------------------------------------------------------
    # Retrieve all return events for MeaningOrgan
    # ---------------------------------------------------------
    def get_returns(self):
        return list(self._returns)

    # ---------------------------------------------------------
    # Clear returns after MeaningOrgan consumes them
    # ---------------------------------------------------------
    def clear_returns(self):
        self._returns = []

    # ---------------------------------------------------------
    # Update circadian state from AirCycleOrgan
    # ---------------------------------------------------------
    def update_circadian(self, circadian_state):
        """
        circadian_state = {
            "day_intensity": float,
            "night_intensity": float,
            "circadian_phase": float,
            "is_day": bool,
            "is_night": bool
        }
        """
        self._circadian.update(circadian_state)

    # ---------------------------------------------------------
    # Retrieve circadian state for MeaningOrgan or OceanOrgan
    # ---------------------------------------------------------
    def get_circadian(self):
        return dict(self._circadian)
