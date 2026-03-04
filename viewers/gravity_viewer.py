# ============================================================
# GRAVITY VIEWER — SHOWS PACKET MASS, DENSITY, AND FLOW
# ============================================================

class GravityViewer:
    """
    Displays a simple gravitational interpretation of packets.
    This viewer never crashes and always returns a list of strings.
    """

    def __init__(self, creature):
        self.creature = creature

    # --------------------------------------------------------
    # Required by Creature.run()
    # --------------------------------------------------------
    def render(self, packets):
        """
        packets: list of packet dicts
        returns: list of strings to print
        """

        if not packets:
            return ["[gravity] no packets"]

        packet = packets[-1]  # most recent packet

        lines = []
        lines.append("=== GRAVITY VIEWER ===")

        # Mass = number of keys
        mass = len(packet)
        lines.append(f"mass: {mass}")

        # Density = number of non-empty values
        density = sum(1 for v in packet.values() if v)
        lines.append(f"density: {density}")

        # Show packet keys
        keys = ", ".join(packet.keys()) if packet else "(none)"
        lines.append(f"fields: {keys}")

        # Show sentence if present
        if "sentence" in packet:
            lines.append(f"sentence: {packet['sentence']}")

        # Show vocabulary frame if present
        if "vocabulary" in packet:
            vocab = packet["vocabulary"]
            lines.append(f"lexical reservoir: {len(vocab.get('lexical', []))} words")

        return lines
