# ascencio_organ.py
# ============================================================
#  ASCENSION ORGAN v2 (Ascensio)
#  - 11 Levels × 17 Micro-Gates
#  - Driven by MathBlockForceCore forces
#  - Fully bus-connected (Command, Force, Packet)
# ============================================================

from dataclasses import dataclass

FORCE_NAMES = [
    "spark",
    "drift",
    "echo",
    "chaos",
    "clarity",
    "memory",
    "pressure",
]

class AscensioOrgan:

    LEVELS = 11
    GATES = 17

    def __init__(self, command_bus, force_bus, packet_bus, name="AscensioOrgan"):
        self.name = name
        self.command_bus = command_bus
        self.force_bus = force_bus
        self.packet_bus = packet_bus

        # Build thresholds once
        self.thresholds = self._build_thresholds()

        # Attach to buses
        self.command_bus.register("ascend", self.handle_command)
        self.command_bus.register("ascensio", self.handle_command)
        self.force_bus.register(self.receive_block)

    # --------------------------------------------------------
    # Threshold table
    # --------------------------------------------------------
    def _build_thresholds(self):
        out = {}
        for lvl in range(1, self.LEVELS + 1):
            base = 0.08 * lvl
            out[lvl] = {
                "spark": base,
                "drift": 0.03 * lvl,
                "echo": base,
                "chaos": 0.02 * lvl,
                "clarity": base,
                "memory": base,
                "pressure": base + 0.04 * lvl,
            }
        return out

    # --------------------------------------------------------
    # Command handler (manual developmental push)
    # --------------------------------------------------------
    def handle_command(self, packet):
        # Optional: could force a developmental step
        pass

    # --------------------------------------------------------
    # Receive MathBlock from Force Bus
    # --------------------------------------------------------
    def receive_block(self, block):
        if block is None:
            return

        # Only developmental logic now — forces come from governing core
        self._advance(block)

    # --------------------------------------------------------
    # Developmental ladder
    # --------------------------------------------------------
    def _advance(self, block):
        if block.ascended:
            return

        # Try to pass current micro-gate
        if self._gate_pass(block):
            block.micro_gate += 1

            # Emit development step packet
            self._emit_development_packet(block)

            # Level up
            if block.micro_gate >= self.GATES:
                block.level += 1
                block.micro_gate = 0

                # Emit level-up packet
                self._emit_development_packet(block)

                # Try ascension at max level
                if block.level >= self.LEVELS:
                    self._try_ascend(block)

    # --------------------------------------------------------
    # Gate passing logic
    # --------------------------------------------------------
    def _gate_pass(self, block):
        f = block.forces.as_dict()
        lvl = block.level
        idx = block.micro_gate

        name = FORCE_NAMES[idx % len(FORCE_NAMES)]
        val = f[name]
        req = self.thresholds[lvl][name]

        return val >= req

    # --------------------------------------------------------
    # Ascension + Canonization
    # --------------------------------------------------------
    def _try_ascend(self, block):
        f = block.forces.as_dict()

        # Ascension requires all forces >= 0.1
        if all(v >= 0.1 for v in f.values()):
            if block.forces.magnitude() >= 1.0:
                block.ascended = True
                self._emit_ascension_packet(block)

        # Canonization requires high pressure
        if f["pressure"] >= 2.0:
            block.canon = True
            self._emit_canon_packet(block)

    # --------------------------------------------------------
    # Packet emissions
    # --------------------------------------------------------
    def _emit_development_packet(self, block):
        packet = {
            "type": "development_step",
            "source": self.name,
            "word": block.word,
            "level": block.level,
            "micro_gate": block.micro_gate,
            "forces": block.forces.as_dict(),
        }
        self.packet_bus.emit(packet)

    def _emit_ascension_packet(self, block):
        packet = {
            "type": "ascension",
            "source": self.name,
            "word": block.word,
            "level": block.level,
            "glyphs": block.glyphs,
            "forces": block.forces.as_dict(),
        }
        self.packet_bus.emit(packet)

    def _emit_canon_packet(self, block):
        packet = {
            "type": "canon",
            "source": self.name,
            "word": block.word,
            "level": block.level,
            "glyphs": block.glyphs,
            "forces": block.forces.as_dict(),
        }
        self.packet_bus.emit(packet)
