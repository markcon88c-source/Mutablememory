import numpy as np

# Global dictionary of symbol → vector
alphabet = {}

# Size of each symbol vector
VECTOR_SIZE = 32

def ensure_symbol(sym):
    """
    Guarantee that a symbol exists in the alphabet.
    If missing, create a new random vector.
    """
    if sym not in alphabet:
        alphabet[sym] = np.random.randn(VECTOR_SIZE)

def get_vector(sym):
    """
    Return the vector for a symbol.
    Ensures the symbol exists first.
    """
    ensure_symbol(sym)
    return alphabet[sym]

def has_symbol(sym):
    """
    Check if a symbol already exists.
    """
    return sym in alphabet

def all_symbols():
    """
    Return a list of all known symbols.
    """
    return list(alphabet.keys())

def alphabet_size():
    """
    Return the number of symbols stored.
    """
    return len(alphabet)






