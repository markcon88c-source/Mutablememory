# ============================================================
# UNIVERSAL BUS ORGAN — Advanced Proto‑Packet Routing
# ============================================================

class UniversalBusOrgan:
    def __init__(self):
        self.subscribers = []
        self.debug_mode = False   # DEBUG OFF BY DEFAULT

    # --------------------------------------------------------
    # Toggle debug mode at runtime
    # --------------------------------------------------------
    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        state = "ON" if self.debug_mode else "OFF"
        print(f"[BUS DEBUG] Debug mode is now {state}")

    # --------------------------------------------------------
    # Register any organ or viewer with a receive() method
    # --------------------------------------------------------
    def register(self, component):

        # BLOCK STORY ORGAN CLEANLY
        if component.__class__.__name__ == "StoryOrgan":
            if self.debug_mode:
                print("[BUS REGISTER] StoryOrgan (blocked)")
            return

        self.subscribers.append(component)

        if self.debug_mode:
            print(f"[BUS REGISTER] {component.__class__.__name__}")

    # --------------------------------------------------------
    # Emit packet into the Cathedral bloodstream
    # --------------------------------------------------------
    def emit(self, packet=None, source=None, channel=None, kind=None, payload=None):

        # Normalize packet if emitted in legacy style
        if packet is None:
            packet = {
                "source": source,
                "channel": channel,
                "kind": kind,
                "payload": payload,
            }

        ptype = packet.get("type", "unknown")

        # ----------------------------------------------------
        # DEBUG: classify packet types
        # ----------------------------------------------------
        if self.debug_mode:
            if ptype.startswith("proto_"):
                print(f"[PROTO] {packet}")
            elif ptype in ("semantic", "sentence", "language"):
                print(f"[HIGH] {packet}")
            else:
                print(f"[BUS] {packet}")

        # ----------------------------------------------------
        # Dispatch to all subscribers
        # ----------------------------------------------------
        for sub in self.subscribers:
            receive_fn = getattr(sub, "receive", None)
            if callable(receive_fn):
                try:
                    if self.debug_mode:
                        print(f"[BUS → {sub.__class__.__name__}] type={ptype}")
                    receive_fn(packet)
                except Exception as e:
                    print(f"[BUS ERROR] {sub.__class__.__name__}.receive failed:", e)
