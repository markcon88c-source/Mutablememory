# ============================================================
#  WIRING MAIN – v1.0
#  Dedicated main for the Wiring Viewer
# ============================================================

import time
import os
import sys

from creature_state import load_state, save_state
from main_support.main_switcher import switch_to

# Import the Creature
from main import Creature


def clear_screen():
    os.system("clear")


def run_wiring_main():
    creature = Creature()

    try:
        load_state(creature)
    except Exception:
        pass

    try:
        while True:
            clear_screen()
            creature.heartbeat()
            creature.wiring_viewer.show()
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

    try:
        save_state(creature)
    except Exception:
        pass


if __name__ == "__main__":
    run_wiring_main()
