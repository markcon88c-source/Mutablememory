import random

class NameGenerator:
    def __init__(self, creature, rate=5):
        """
        rate = number of ticks between name generations
        """
        self.creature = creature
        self.rate = rate
        self.counter = 0

    def tick(self):
        self.counter += 1
        if self.counter >= self.rate:
            self.counter = 0
            self.generate_and_send()

    def generate_and_send(self):
        # 1. Generate a name
        name = self._generate_name()

        # 2. Choose parent blocks
        parents = self._choose_parent_blocks()

        # 3. Birth the math block (this triggers the Cathedral)
        try:
            self.creature.mathblocks.birth_block_from_name(name, parents)
        except Exception as e:
            print(f"[NAMEGEN ERROR] Failed to birth '{name}': {e}")

    # -----------------------------------------------------
    # NAME GENERATION (placeholder — plug in your generator)
    # -----------------------------------------------------
    def _generate_name(self):
        syllables = ["va", "lo", "ren", "ka", "shi", "dra", "mor", "el", "tha"]
        name = random.choice(syllables) + random.choice(syllables)
        return name.capitalize()

    # -----------------------------------------------------
    # PARENT BLOCK SELECTION
    # -----------------------------------------------------
    def _choose_parent_blocks(self):
        blocks = self.creature.mathblocks.blocks
        if len(blocks) < 2:
            return random.sample(blocks, len(blocks)) if blocks else []
        return random.sample(blocks, 2)
