# run_command_bus.py
# ============================================================
# COMMAND BUS TEST HARNESS (ISOLATED)
# Feeds python-like commands into CommandBuilderOrgan and
# prints normalized "go" action packets.
# ============================================================

import time

from organs.command_builder_organ import CommandBuilderOrgan


# ------------------------------------------------------------
# Minimal PacketBus for testing
# ------------------------------------------------------------
class PacketBus:
    def __init__(self):
        self._packets = []

    def send(self, packet):
        self._packets.append(packet)

    def collect(self, packet_type):
        out = [p for p in self._packets if p["type"] == packet_type]
        self._packets = []
        return out


# ------------------------------------------------------------
# Minimal Creature Stub
# ------------------------------------------------------------
class TestCreature:
    def __init__(self):
        self.bus = PacketBus()
        self.organs = [
            CommandBuilderOrgan(self)
        ]


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
def main():
    creature = TestCreature()

    print("=== ⚡ COMMAND BUS VIEWER ===")

    # A rotating list of python-like commands
    commands = [
        "step", "call", "update", "run", "process", "emit",
        "tick", "pulse", "advance", "think", "cycle", "build",
        "translate", "compute", "apply", "execute", "invoke",
        "trigger", "fire", "go", "anything"
    ]

    index = 0

    while True:
        raw_cmd = commands[index % len(commands)]
        index += 1

        # Feed the organ a python-like command
        thought = {
            "command": raw_cmd
        }

        # Step the organ
        for organ in creature.organs:
            if hasattr(organ, "step"):
                organ.step(thought, {}, {}, {})

        # Collect command packets
        packets = creature.bus.collect("command")

        if packets:
            for p in packets:
                action = p["data"]["action"]
                raw = p["data"]["raw"]
                print(f"[command] action={action} raw={raw}")
        else:
            print("(no command packets)")

        print("==============================")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
