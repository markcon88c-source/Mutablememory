# mathblock_force_core.py
# Governing substrate for MathBlocks

from math import sqrt
import random

class Forces:
    def __init__(self, spark=0, drift=0, echo=0, chaos=0, clarity=0, memory=0, pressure=0):
        self.spark = spark
        self.drift = drift
        self.echo = echo
        self.chaos = chaos
        self.clarity = clarity
        self.memory = memory
        self.pressure = pressure

    def as_dict(self):
        return {
            "spark": self.spark,
            "drift": self.drift,
            "echo": self.echo,
            "chaos": self.chaos,
            "clarity": self.clarity,
            "memory": self.memory,
            "pressure": self.pressure,
        }

    def magnitude(self):
        d = self.as_dict()
        return sqrt(sum(v * v for v in d.values()))


class MathBlock:
    def __init__(self, word):
        self.word = word
        self.forces = Forces()
        self.level = 1
        self.micro_gate = 0
        self.ascended = False
        self.canon = False
        self.glyphs = []
        self.semantic_vector = []


class MathBlockForceCore:

    def __init__(self):
        self.registry = {}

    def get_or_create_block_for_word(self, word):
        if word not in self.registry:
            self.registry[word] = MathBlock(word)
        return self.registry[word]

    def update_block(self, block):
        # Simple force update — downstream organs do the real work
        block.forces.spark = random.uniform(0.0, 1.0)
        block.forces.drift = random.uniform(0.0, 1.0)
        block.forces.echo = random.uniform(0.0, 1.0)
        block.forces.chaos = random.uniform(0.0, 1.0)
        block.forces.clarity = random.uniform(0.0, 1.0)
        block.forces.memory = random.uniform(0.0, 1.0)
        block.forces.pressure = random.uniform(0.0, 1.0)

        return block

    def sample_word(self):
        # Simple placeholder — replace with your vocabulary logic
        if not self.registry:
            return "begin"
        return random.choice(list(self.registry.keys()))
