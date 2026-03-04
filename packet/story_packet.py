class StoryPacket:
    def __init__(self, source=None, meaning=None, structure=None, metadata=None):
        self.source = source
        self.meaning = meaning
        self.structure = structure
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<StoryPacket source={self.source} meaning={self.meaning}>"
