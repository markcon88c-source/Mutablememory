class Character:
    def __init__(self, nameheart, spark, forces, wounds=None):
        self.nameheart = nameheart        # mythic + proto names
        self.spark = spark                # creative spark / birth spark
        self.forces = forces              # dictionary of forces
        self.wounds = wounds or []        # emotional wounds
        self.quests = []                  # quests assigned
        self.id = f"{nameheart['mythic']}-{nameheart['proto']}"
