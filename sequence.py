import numpy as np
from config import MAX_BLOCK_LEN, steps
from memory import memory_to_letter, update_memory
from alphabet import alphabet, ensure_symbol
from mood import compute_entropy, update_mood, build_decorated_blocks

target = np.array([0.3, -0.1, 0.2])

def generate_sequence():
    seq = []
    for t in range(steps):
        bl = np.random.randint(1, MAX_BLOCK_LEN + 1)
        letters = []
        for i in range(bl):
            L = memory_to_letter()
            letters.append(L)
            x = alphabet[L]
            update_memory(x, target)
        seq.append("".join(letters))
    return seq
