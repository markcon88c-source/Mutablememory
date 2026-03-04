class BaseOrgan:
    """
    Modern Cathedral BaseOrgan.
    All organs must accept (packet) in step().
    """
    def __init__(self, creature=None):
        self.creature = creature

    def step(self, packet):
        """
        Default organ behavior.
        Override in child organs.
        """
        return packet
