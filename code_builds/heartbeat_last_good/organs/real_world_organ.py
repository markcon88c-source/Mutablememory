import random

class RealWorldOrgan:
    def __init__(self):
        # Real-world entities
        self.entities = [
            "a dog",
            "a human",
            "a bird",
            "a tree",
            "a river",
            "the wind",
            "a stone",
            "a shadow",
            "a fox",
            "a lantern",
            "a doorway",
            "a fire",
        ]

        # Real-world actions
        self.actions = [
            "barks",
            "watches",
            "approaches",
            "waits",
            "listens",
            "moves",
            "circles",
            "rests",
            "murmurs",
            "shifts",
            "glows",
            "flickers",
            "leans",
        ]

    def generate(self, state):
        entity = random.choice(self.entities)
        action = random.choice(self.actions)

        phrase = f"{entity} {action}"

        return {
            "entity": entity,
            "action": action,
            "phrase": phrase
        }
