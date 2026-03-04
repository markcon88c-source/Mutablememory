# viewer.py — English/state viewer for drift, pressure, mood, thought, world, heart

def print_state(state):
    print("\n⏱  Tick:", state["tick"])
    print("========================================")

    # 🌩 Drift
    drift = state["drift"]
    print(f"🌩 Drift:    {drift}")

    # 🧘 Calm / Pressure
    pressure = state["pressure"]
    if isinstance(pressure, dict):
        calm = pressure.get("calm", 0.0)
        symbolic = pressure.get("symbolic", 0.0)
        alert = pressure.get("alert", 0.0)

        calm_bar = _bar(calm)
        sym_bar = _bar(symbolic)
        alert_bar = _bar(alert)

        print(f"🧘 Calm:      {calm:.2f}   {calm_bar}")
        print(f"🔣 Symbolic:  {symbolic:.2f}   {sym_bar}")
        print(f"⚡ Alert:     {alert:.2f}   {alert_bar}")

    # 😊 Mood
    print(f"😊 Mood:     {state['mood']}")

    # 🧠 Thought
    print(f"🧠 Thought:  {state['thought']}")

    # 🌍 World
    print(f"🌍 World:    {state['world']}")

    # ❤️ Heart
    heart = state["heart"]
    if isinstance(heart, dict):
        print(f"❤️ Heart:    {heart.get('cluster', '?')}  (beat {state['tick']})")
        meaning = heart.get("meaning", {})
        print(f"   ↳ word:    {meaning.get('word')}")
        print(f"   ↳ concept: {meaning.get('concept')}")

    print("========================================")


def _bar(value):
    """Simple 20-char bar for calm/symbolic/alert."""
    filled = int(value * 20)
    return "[" + ("█" * filled) + ("-" * (20 - filled)) + "]"
