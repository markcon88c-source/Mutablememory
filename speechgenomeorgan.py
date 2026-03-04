class SpeechGenomeOrgan:
    def __init__(self, genome):
        self.genome = genome

    def pick_line(self, mode, category, speaker_block):
        import random

        # Weighting based on math forces
        force = speaker_block.get_force_for(category)

        options = self.genome[mode][category]

        # Weighted random choice
        index = int((force * (len(options)-1)))
        index = max(0, min(index, len(options)-1))

        return options[index]
