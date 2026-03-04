# run_creature.py
# Minimal launcher for the full creature (router + ocean + metabolism)

from creature import Creature
import time

creature = Creature()

print("\n=== CREATURE ROUTER MODE ===")
print("Press CTRL+C to exit.\n")

while True:
    try:
        # Run one heartbeat
        creature.step()

        # Slow the output slightly so it's readable
        time.sleep(0.15)

    except KeyboardInterrupt:
        print("\nExiting Creature Router Mode.")
        break
    except Exception as e:
        print(f"[Creature Error] {e}")
        time.sleep(0.5)
