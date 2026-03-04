# organs/word_importer.py

import random

class WordImporter:
    """
    Slowly releases words and names from the repository into L1.
    Handles:
      • normal vocabulary trickle
      • rare name introduction
      • math‑block‑crafted name generation
      • cooldown pacing to prevent flooding
    """

    def __init__(self, creature):
        self.creature = creature
        self.cooldown = 0

    def tick(self):
        """
        Called every heartbeat.
        Controls the slow, mythic introduction of new words.
        """

        # -----------------------------------------------------
        # COOLDOWN — prevents flooding the STM
        # -----------------------------------------------------
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        # -----------------------------------------------------
        # 1) NORMAL WORD IMPORT (5% chance)
        # -----------------------------------------------------
        if random.random() < 0.05:
            word = self.creature.word_repository.get_random_word()
            if word:
                # Assign math block identity to the word
                self.creature.mathblocks.get_mathblock_for_word(word)

                # Add to STM at the lowest level
                self.creature.stm.add_word(word)

                # Slow the flow
                self.cooldown = random.randint(5, 15)
                return

        # -----------------------------------------------------
        # 2) MATH‑BLOCK‑CRAFTED NAME IMPORT (0.5% chance)
        # -----------------------------------------------------
        if random.random() < 0.005:
            # Generate a new name from math blocks
            name = self.creature.word_repository.generate_mathblock_name(self.creature)

            # The name generator already performs the birth ritual:
            #   • blends parent blocks
            #   • creates a new math block
            #   • assigns name → new block
            # So we only need to add it to STM.

            self.creature.stm.add_word(name)

            # Names should be rare mythic events
            self.cooldown = random.randint(20, 40)
            return

        # -----------------------------------------------------
        # 3) USER‑DEFINED NAMES (1% chance)
        # -----------------------------------------------------
        # If the user adds names manually, they should also trickle in.
        if self.creature.word_repository.names and random.random() < 0.01:
            name = self.creature.word_repository.get_random_name()

            # Assign math block identity
            self.creature.mathblocks.get_mathblock_for_word(name)

            # Add to STM
            self.creature.stm.add_word(name)

            self.cooldown = random.randint(10, 25)
            return



