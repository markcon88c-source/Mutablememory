# WORLDBUILDING LENS ORGAN — CATHEDRAL EDITION
# Assigns world-anchors, domains, and contextual placement to identities, packets, and characters.

class WorldbuildingLensOrgan:
    def __init__(self, creature):
        self.creature = creature
        self.last_assignment = None

    def assign_anchors(self, identity):
        """
        Assign world anchors to an identity or packet.
        Identity may be:
        - a dict with "name"
        - a packet object with .name or .text
        - a raw string
        """

        # Extract name
        name = None

        if isinstance(identity, dict):
            name = identity.get("name")

        elif isinstance(identity, str):
            name = identity

        else:
            # Packet-like object
            if hasattr(identity, "name"):
                name = identity.name
            elif hasattr(identity, "text"):
                name = identity.text

        # Default anchor structure
        anchors = {
            "domain": "neutral",
            "region": "unplaced",
            "tags": [],
        }

        # Simple domain logic (expand later)
        if name:
            lowered = name.lower()

            if lowered.startswith("d"):
                anchors["domain"] = "dawn"

            elif lowered.startswith("c"):
                anchors["domain"] = "cash"

            else:
                anchors["domain"] = "neutral"

        self.last_assignment = anchors
        return anchors

    def tick(self):
        return self.last_assignment
