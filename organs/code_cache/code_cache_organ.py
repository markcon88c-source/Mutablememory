#!/usr/bin/env python3

class CodeCache:
    """
    Stores the latest code for all organs.
    """
    def __init__(self):
        self.cache = {}

    def update(self, name, code):
        self.cache[name] = code

    def get(self, name):
        return self.cache.get(name, None)

    def all(self):
        return self.cache
