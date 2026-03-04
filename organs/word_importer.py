import random

class WordImporter:
    """
    Slowly releases words and names from the repository into L1.
    """

    def __init__(self, creature):
        self.creature = creature
        self.cooldown = 0

    def tick(self):
        # Cooldown prevents flooding
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        # 5% chance to import a normal word
        if random.random() < 0.05:
            word = self.creature.word_repository.get_random_word()
            if word:
                self.creature.stm.add_word(word)
                self.cooldown = random.randint(5, 15)
                return

        # 0.5% chance to import a character name
        if random.random() < 0.005:
            name = self.creature.word_repository.get_random_name()
            if name:
                self.creature.stm.add_word(name)
                self.cooldown = random.randint(20, 40)
                return
