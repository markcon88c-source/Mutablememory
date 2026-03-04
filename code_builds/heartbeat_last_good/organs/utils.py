import numpy as np

def clip_grad(x, limit):
    n = np.linalg.norm(x)
    if n > limit and n > 0:
        return x * (limit / n)
    return x

def limit_norm(x, max_norm):
    n = np.linalg.norm(x)
    if n > max_norm and n > 0:
        return x * (max_norm / n)
    return x

def soft_damp(x, scale):
    return np.tanh(x / scale) * scale
