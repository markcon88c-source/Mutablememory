# main_support/main_heartbeat.py
# Human‑eye‑friendly heartbeat loop for the Creature

from creature import Creature
import time

# ------------------------------------------------------------
# HEARTBEAT SPEED SETTINGS
# ------------------------------------------------------------
# Choose ONE of these speeds by uncommenting it:

HEARTBEAT_DELAY = 2.0      # Calm, readable, natural breathing
# HEARTBEAT_DELAY = 3.5    # Slow, mythic, ceremonial
# HEARTBEAT_DELAY = 1.2    # Medium, readable but lively
# HEARTBEAT_DELAY = 0.5    # Fast (original speed)
# HEARTBEAT_DELAY = 0.1    # Hyper mode (not human friendly)

# ------------------------------------------------------------
# OPTIONAL: MANUAL STEP MODE
# ------------------------------------------------------------
# Set to True if you want to press Enter for each heartbeat.
MANUAL_STEP = False


def main():
    creature = Creature()
    cycle = 1

    while True:
        print(f"\n\n🌿 HEARTBEAT CYCLE {cycle}")
        print("────────────────────────────────────────")

        creature.step()

        if MANUAL_STEP:
            input("\nPress Enter for next heartbeat...")
        else:
            time.sleep(HEARTBEAT_DELAY)

        cycle += 1


if __name__ == "__main__":
    main()
