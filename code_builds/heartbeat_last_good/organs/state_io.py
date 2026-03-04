import numpy as np
import os

def save_array(name, arr):
    np.save(name + ".npy", arr)

def load_array(name, default):
    fname = name + ".npy"
    if os.path.exists(fname):
        return np.load(fname)
    return default

def save_cycle_counter(n):
    save_array("cycle_counter", np.array([n]))

def load_cycle_counter():
    arr = load_array("cycle_counter", np.array([0]))
    return int(arr[0])

def save_mood_index(m):
    save_array("mood_index", np.array([m]))

def load_mood_index():
    arr = load_array("mood_index", np.array([2.0]))
    return float(arr[0])
