class WorldbuildingOrgan:
    """
    Mid-layer worldbuilding engine.
    Takes world-ideas and produces structured worldbuilding nodes.
    Maintains b_s (short-term) and b_l (long-term) worldbuilding.
    Emits packets for viewers and downstream organs.
    """

    def __init__(self, creature):
        self.creature = creature

        # short-term worldbuilding (volatile)
        self.b_s = []

        # long-term worldbuilding (canon)
        self.b_l = []

        # active worldbuilding idea
        self.active = None

    def accept(self, packet):
        ptype = packet.get("type")

        # world-idea from WorldIdeaOrgan
        if ptype == "world_idea":
            idea = packet.get("payload", {})
            self.process_world_idea(idea)

    def process_world_idea(self, idea):
        # promote idea to active
        self.active = idea

        # short-term memory
        self.b_s.append(idea)
        if len(self.b_s) > 12:
            self.b_s.pop(0)

        # long-term memory (slow accumulation)
        if idea.get("weight", 0) > 0.7:
            self.b_l.append(idea)

        # emit worldbuilding packet
        self.creature.bus.emit({
            "type": "worldbuilding",
            "payload": {
                "b_s": self.b_s,
                "b_l": self.b_l,
                "active": self.active,
            }
        })

    def tick(self):
        pass
