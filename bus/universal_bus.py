# ============================================================
# UNIVERSAL BUS — the one actually used by Creature
# ============================================================

class UniversalBus:
    def __init__(self, creature):
        self.creature = creature

        # Organs registered here
        self.registry = {}

        # Packet history
        self.history = []

        # Last broadcast packet
        self.last_broadcast = None

        # Message log (DiagnosticViewer expects this)
        self.message_log = []

    # --------------------------------------------------------
    # Register an organ
    # --------------------------------------------------------
    def register(self, organ):
        name = organ.__class__.__name__

        # BLOCK STORY ORGAN CLEANLY
        if name == "StoryOrgan":
            return

        self.registry[name] = organ

    # --------------------------------------------------------
    # Emit a packet
    # --------------------------------------------------------
    def emit(self, source, channel, kind, payload):
        packet = {
            "source": source,
            "channel": channel,
            "kind": kind,
            "payload": payload,
        }

        # Add to history
        self.history.append(packet)
        self.last_broadcast = packet

        # Add to message log
        self.message_log.append(packet)
        if len(self.message_log) > 200:
            self.message_log.pop(0)

        # Trim history
        if len(self.history) > 200:
            self.history.pop(0)

    # --------------------------------------------------------
    # Drive organs
    # --------------------------------------------------------
    def tick(self):
        for organ in self.registry.values():

            # Cathedral-style tick(self)
            if hasattr(organ, "tick"):
                try:
                    organ.tick()
                except TypeError:
                    # Some organs define tick(self, creature)
                    try:
                        organ.tick(self.creature)
                    except Exception:
                        pass
                continue

            # Experimental-Wall tick_legacy(self, creature)
            if hasattr(organ, "tick_legacy"):
                try:
                    organ.tick_legacy(self.creature)
                except Exception:
                    pass
                continue

            # Very old organ style
            if hasattr(organ, "step"):
                try:
                    organ.step()
                except Exception:
                    pass
                continue

            # Passive organ — skip safely
            pass

    # --------------------------------------------------------
    # Snapshot for viewers
    # --------------------------------------------------------
    def snapshot(self):
        return {
            "registry": list(self.registry.keys()),
            "organs": list(self.registry.keys()),
            "packets": list(self.history),
            "last_broadcast": self.last_broadcast,
            "message_log": list(self.message_log),
        }
