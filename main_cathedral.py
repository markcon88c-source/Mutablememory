from main import Creature
from organs.cathedral_viewer import CathedralViewer
import time
import os

def clear_screen():
    os.system("clear")

def main():
    creature = Creature()
    viewer = CathedralViewer(creature)

    while True:
        clear_screen()
        creature.heartbeat()
        viewer.show()
        time.sleep(0.1)
