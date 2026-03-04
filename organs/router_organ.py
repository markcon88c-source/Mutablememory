class RouterOrgan:
    """
    Cathedral Router Organ.
    Central coordinator of the metabolic chain.
    Routes the FieldPacket through all organs in the correct order.
    """

    def __init__(self, creature):
        self.creature = creature
        self.organ_chain = []

        # If the creature defines an organ list, use it automatically.
        if hasattr(creature, "organs") and isinstance(creature.organs, list):
            self.organ_chain = creature.organs

    def register_organs(self, organs):
        """
        Manually register a list of organs in metabolic order.
        """
        self.organ_chain = organs

    def tick(self, iteration, packet):
        """
        Pass the FieldPacket through each organ in sequence.
        """
        if packet is None:
            packet = {}

        routing_log = []

        for organ in self.organ_chain:
            name = organ.__class__.__name__
            try:
                packet = organ.tick(iteration, packet)
                routing_log.append({"organ": name, "status": "ok"})
            except Exception as e:
                routing_log.append({"organ": name, "status": "error", "error": str(e)})
                packet["router_error"] = {
                    "organ": name,
                    "error": str(e)
                }
                break

        packet["router"] = {
            "iteration": iteration,
            "chain_length": len(self.organ_chain),
            "log": routing_log
        }

        return packet
