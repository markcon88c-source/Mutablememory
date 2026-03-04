# organs/mathblock_field.py
# Unified mathblock field with four liquid states.
# SAFE: does nothing unless explicitly stepped.

import random
import math

class MathBlockField:
    """
    A unified field where mathblocks behave like particles in a liquid.
    Four states:
      - calm
      - storm
      - plasma
      - gel

    Words react based on their own forces multiplied by the environment.
    """

    def __init__(self, creature):
        self.creature = creature
        self.blocks = []          # all mathblocks in the field
        self.positions = {}       # block_id -> (x, y)
        self.velocities = {}      # block_id -> (vx, vy)
        self.environment = "calm" # default, inert
        self.active = False       # field is OFF until activated

        # environment multipliers
        self.env = {
            "calm":   {"spark": 0.4, "drift": 0.2, "echo": 0.6, "pressure": 0.3, "viscosity": 0.8},
            "storm":  {"spark": 1.2, "drift": 1.5, "echo": 0.8, "pressure": 1.3, "viscosity": 0.3},
            "plasma": {"spark": 2.0, "drift": 1.8, "echo": 1.6, "pressure": 1.7, "viscosity": 0.1},
            "gel":    {"spark": 0.7, "drift": 0.1, "echo": 1.8, "pressure": 0.5, "viscosity": 1.5},
        }

    # ------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------
    def activate(self):
        """Turn the field ON."""
        self.active = True

    def deactivate(self):
        """Turn the field OFF."""
        self.active = False

    def set_environment(self, env_name):
        """Switch between calm, storm, plasma, gel."""
        if env_name in self.env:
            self.environment = env_name

    def add_blocks(self, blocks):
        """Add mathblocks to the field."""
        for b in blocks:
            block_id = id(b)
            self.blocks.append(b)
            self.positions[block_id] = (random.random(), random.random())
            self.velocities[block_id] = (0.0, 0.0)

    # ------------------------------------------------------------
    # HEARTBEAT STEP (SAFE unless activated)
    # ------------------------------------------------------------
    def step(self):
        """Advance the field one tick."""
        if not self.active:
            return  # SAFE: do nothing

        env = self.env[self.environment]

        for b in self.blocks:
            block_id = id(b)

            # extract forces
            spark = b.get("spark", 0.0)
            drift = b.get("drift", 0.0)
            echo = b.get("echo", 0.0)
            pressure = b.get("pressure", 0.0)

            # environment multipliers
            fx = (spark * env["spark"]) - (drift * env["drift"])
            fy = (echo * env["echo"]) - (pressure * env["pressure"])

            # update velocity
            vx, vy = self.velocities[block_id]
            vx += fx * 0.01
            vy += fy * 0.01

            # apply viscosity
            vx *= env["viscosity"]
            vy *= env["viscosity"]

            # update position
            x, y = self.positions[block_id]
            x += vx
            y += vy

            # wrap-around boundary
            x %= 1.0
            y %= 1.0

            # store
            self.velocities[block_id] = (vx, vy)
            self.positions[block_id] = (x, y)
