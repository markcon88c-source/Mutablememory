from main import Creature
from organs.receiving_room_viewer import ReceivingRoomViewer
import time
import os

def clear_screen():
    os.system("clear")

def main():
    creature = Creature()
    viewer = ReceivingRoomViewer(creature)

    PHASE_TIME = 10.0
    last_phase_switch = time.time()
    phase = "diagnostics"

    # Draw immediately on start
    clear_screen()
    viewer.show_diagnostics()
    print("\n(Interactions in 10 seconds...)")

    while True:
        now = time.time()

        # Heartbeat always runs
        creature.heartbeat()

        # Switch phases every 10 seconds
        if now - last_phase_switch >= PHASE_TIME:
            phase = "interactions" if phase == "diagnostics" else "diagnostics"
            last_phase_switch = now

            clear_screen()

            if phase == "diagnostics":
                viewer.show_diagnostics()
                print("\n(Interactions in 10 seconds...)")
            else:
                viewer.show_interactions()
                print("\n(Diagnostics in 10 seconds...)")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
