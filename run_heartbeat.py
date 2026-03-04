import time
import os
from creature import Creature

def main():
    creature = Creature()
    while True:
        os.system("clear")
        packet = creature.heartbeat()
        print("Heartbeat:", creature.iteration)
        time.sleep(1)

if __name__ == "__main__":
    main()
