# organs/pressure_placeholders.py

def make_pressure_placeholder(name: str) -> dict:
    """
    Full future-proof pressure schema.
    Works for ALL pressures: alert, calm, storm, symbolic, concentration, word_strength.
    """
    return {
        "name": name,

        # --- Core pressure value ---
        "value": 0.0,          # main pressure (0–1)
        "delta": 0.0,          # change since last tick
        "accel": 0.0,          # change of the change
        "tone": "steady",      # rising / falling / steady
        "reason": "placeholder",

        # --- Sub-pressures (room to grow) ---
        "sub": {
            "instability": 0.0,
            "stability": 0.0,
            "memory": 0.0,
            "chaos": 0.0,
            "symbolic": 0.0,
            "storm": 0.0,
            "focus": 0.0,
            "rarity": 0.0,
        },

        # --- Meta (room for future organs) ---
        "meta": {
            "source": "placeholder",
            "confidence": 1.0,
            "volatility": 0.0,
            "saturation": 0.0,
            "history": [],      # future: pressure history
            "peaks": [],        # future: peak detection
            "valleys": [],      # future: collapse detection
        }
    }


def make_all_pressure_placeholders():
    """
    Returns a full pressure dictionary for the entire pressure ecosystem.
    """
    names = [
        "alert",
        "calm",
        "storm",
        "symbolic",
        "concentration",
        "word_strength",
    ]
    return {name: make_pressure_placeholder(name) for name in names}
