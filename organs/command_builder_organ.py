# COMMAND BUILDER ORGAN — CATHEDRAL EDITION
# Combines thought, world, heart, and memory into a unified command packet.

class CommandBuilderOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.last_command = None

    def step(self, thought, world, heart, memory):
        """
        Build a command packet from the four major subsystems.
        Each subsystem may be None during early boot.
        """

        command = {
            "thought": thought,
            "world": world,
            "heart": heart,
            "memory": memory,
        }

        self.last_command = command
        return command

    def tick(self):
        return self.last_command
