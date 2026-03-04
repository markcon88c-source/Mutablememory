# ============================================================
# COMMAND BUS ORGAN — Cathedral Edition
# ============================================================
# This organ acts as the creature's nervous system:
# - routes commands
# - handles viewer faults
# - handles packet-flow faults
# - handles semantic/narrative/force/metabolic faults
# - prevents tick-method crashes
# ============================================================

class CommandBusOrgan:
    def __init__(self):
        self.subscribers = {}  # pattern → list of callbacks
        self.last_event = None

    # --------------------------------------------------------
    # SUBSCRIBE
    # --------------------------------------------------------
    def subscribe(self, pattern, callback):
        if pattern not in self.subscribers:
            self.subscribers[pattern] = []
        self.subscribers[pattern].append(callback)

    # --------------------------------------------------------
    # EMIT
    # --------------------------------------------------------
    def emit(self, event):
        """
        event example:
            {
                "type": "packet.missing",
                "viewer": "sentence",
                "details": {"field": "tokens"}
            }
        """
        event_type = event.get("type")
        if not event_type:
            return

        self.last_event = event

        for pattern, callbacks in self.subscribers.items():
            if self._matches(pattern, event_type):
                for cb in callbacks:
                    try:
                        cb(event)
                    except Exception as e:
                        self._emit_internal_error(pattern, cb, e)

    # --------------------------------------------------------
    # INTERNAL ERROR EMISSION
    # --------------------------------------------------------
    def _emit_internal_error(self, pattern, callback, exception):
        internal_event = {
            "type": "system.bus_failure",
            "viewer": None,
            "details": {
                "pattern": pattern,
                "callback": str(callback),
                "exception": str(exception)
            }
        }

        # Deliver only to system.* subscribers
        for p, callbacks in self.subscribers.items():
            if self._matches(p, "system.bus_failure"):
                for cb in callbacks:
                    try:
                        cb(internal_event)
                    except:
                        pass

    # --------------------------------------------------------
    # PATTERN MATCHING
    # --------------------------------------------------------
    def _matches(self, pattern, event_type):
        if pattern == "*":
            return True
        if pattern.endswith(".*"):
            prefix = pattern[:-2]
            return event_type.startswith(prefix)
        return pattern == event_type

    # --------------------------------------------------------
    # ORGAN INTERFACE (optional)
    # --------------------------------------------------------
    def tick(self, creature):
        # Command Bus does not emit packets on its own.
        # It only reacts to events.
        return {"event": self.last_event}
