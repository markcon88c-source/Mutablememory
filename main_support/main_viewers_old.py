import sys, os
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
from critter.critter import Creature
from main_support.five_stack_viewer import render
import time

def main():
    creature = Creature()

    while True:
        packet = creature.heartbeat()
        render(packet)
        time.sleep(0.25)

if __name__ == "__main__":
    main()
