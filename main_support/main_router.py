# main_support/main_router.py
# Entry point for the Creature's RouterOrgan

from creature import Creature

def main():
    creature = Creature()
    router = creature.router
    router.run()

if __name__ == "__main__":
    main()
