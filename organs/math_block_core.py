# ============================================================
#  CREATURE PROTOTYPE v0.1
#  - Identity
#  - Math Block Force Core (11×17)
#  - STM Organ (11 levels)
#  - L-Level Organ
#  - Storm Organ
#  - Mood Organ
#  - World Organ
#  - Idea Organ
#  - Story Organ
#  - Viewer Hooks
# ============================================================

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import random
import math

# ------------------------------------------------------------
# 1. IDENTITY CORE
# ------------------------------------------------------------

@dataclass
class IdentityCore:
    vector: List[float] = field(default_factory=lambda: [0.1, 0.1, 0.1])
    chaos_bias: float = 0.0
    memory_depth: float = 0.0

    def similarity(self, vec: List[float]) -> float:
        if not vec:
            return 0.0
        num = sum(a*b for a,b in zip(self.vector, vec))
        den1 = math.sqrt(sum(a*a for a in self.vector))
        den2 = math.sqrt(sum(b*b for b in vec))
        if den1 == 0 or den2 == 0:
            return 0.0
        return num / (den1 * den2)


# ------------------------------------------------------------
# 2. FORCE VECTOR
# ------------------------------------------------------------

FORCE_NAMES = ["spark","drift","echo","chaos","clarity","memory","pressure"]

@dataclass
class ForceVector:
    spark: float = 0.0
    drift: float = 0.0
    echo: float = 0.0
    chaos: float = 0.0
    clarity: float = 0.0
    memory: float = 0.0
    pressure: float = 0.0

    def as_dict(self): return {k:getattr(self,k) for k in FORCE_NAMES}
    def magnitude(self): return math.sqrt(sum(v*v for v in self.as_dict().values()))


# ------------------------------------------------------------
# 3. MATH BLOCK FORCE CORE (11×17)
# ------------------------------------------------------------

@dataclass
class MathBlock:
    core: float
    shell: Dict[str,Any] = field(default_factory=dict)
    semantic_vector: Optional[List[float]] = None

    level: int = 1
    micro_gate: int = 0
    ascended: bool = False
    canon: bool = False

    forces: ForceVector = field(default_factory=ForceVector)
    label: str = ""


class MathBlockForceCore:
    LEVELS = 11
    GATES = 17

    def __init__(self):
        self.thresholds = self._build_thresholds()

    def _build_thresholds(self):
        out = {}
        for lvl in range(1, self.LEVELS+1):
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

    def update(self, block: MathBlock, identity, memory, world):
        block.forces = self.compute_forces(block, identity, memory, world)
        self._advance(block, identity, memory, world)

    def compute_forces(self, block, identity, memory, world):
        core = block.core
        shell = len(block.shell)

        spark = abs(core) * (1 + 0.1*block.level)
        drift = (shell % 5)*0.08 + random.uniform(0,0.04)
        echo = memory.recall + 0.05*memory.ltm
        chaos = world.gremlin + identity.chaos_bias*0.5
        clarity = max(0, 1 - drift - chaos*0.4)
        memf = memory.ltm + memory.stm*0.5
        pressure = abs(core) + shell*0.1 + memf*0.2

        return ForceVector(spark,drift,echo,chaos,clarity,memf,pressure)

    def _advance(self, block, identity, memory, world):
        if block.ascended: return

        if self._gate_pass(block, identity, memory, world):
            block.micro_gate += 1
            if block.micro_gate >= self.GATES:
                block.level += 1
                block.micro_gate = 0

        if block.level >= self.LEVELS:
            self._try_ascend(block, identity, memory, world)

    def _gate_pass(self, block, identity, memory, world):
        f = block.forces.as_dict()
        lvl = block.level
        idx = block.micro_gate
        name = FORCE_NAMES[idx % len(FORCE_NAMES)]
        val = f[name]
        req = self.thresholds[lvl][name]
        return val >= req

    def _try_ascend(self, block, identity, memory, world):
        f = block.forces.as_dict()
        if all(v >= 0.1 for v in f.values()):
            if block.forces.magnitude() >= 1.0:
                block.ascended = True
                if f["pressure"] >= 2.0:
                    block.canon = True


# ------------------------------------------------------------
# 4. STM ORGAN (11 levels)
# ------------------------------------------------------------

@dataclass
class STMOrgan:
    levels: List[List[str]] = field(default_factory=lambda: [[] for _ in range(11)])

    def push(self, word: str):
        self.levels[0].append(word)

    def tick(self):
        for i in reversed(range(1,11)):
            self.levels[i].extend(self.levels[i-1])
        self.levels[0] = []


# ------------------------------------------------------------
# 5. L-LEVEL ORGAN
# ------------------------------------------------------------

@dataclass
class LLevelOrgan:
    levels: Dict[str,int] = field(default_factory=dict)

    def get(self, word): return self.levels.get(word,1)
    def promote(self, word): self.levels[word] = min(11, self.get(word)+1)


# ------------------------------------------------------------
# 6. STORM ORGAN
# ------------------------------------------------------------

@dataclass
class StormOrgan:
    intensity: float = 0.0

    def tick(self):
        self.intensity = max(0, self.intensity + random.uniform(-0.1,0.1))


# ------------------------------------------------------------
# 7. MOOD ORGAN
# ------------------------------------------------------------

@dataclass
class MoodOrgan:
    mood: float = 0.0

    def tick(self):
        self.mood += random.uniform(-0.05,0.05)
        self.mood = max(-1, min(1, self.mood))


# ------------------------------------------------------------
# 8. WORLD ORGAN
# ------------------------------------------------------------

@dataclass
class WorldOrgan:
    pressure: float = 0.0
    gremlin: float = 0.0

    def tick(self):
        self.gremlin = max(0, self.gremlin + random.uniform(-0.05,0.05))


# ------------------------------------------------------------
# 9. IDEA ORGAN
# ------------------------------------------------------------

@dataclass
class IdeaOrgan:
    ideas: List[str] = field(default_factory=list)

    def spawn(self, word):
        if random.random() < 0.1:
            self.ideas.append(f"Idea_of_{word}")


# ------------------------------------------------------------
# 10. STORY ORGAN
# ------------------------------------------------------------

@dataclass
class StoryOrgan:
    last_sentence: str = ""

    def generate(self, mood, storm, ideas):
        tone = "calm" if mood.mood > 0 else "tense"
        storm_tag = "⚡" if storm.intensity > 0.5 else ""
        idea = ideas.ideas[-1] if ideas.ideas else "nothing"
        self.last_sentence = f"The creature feels {tone} {storm_tag} and thinks of {idea}."


# ------------------------------------------------------------
# 11. CREATURE (all organs wired)
# ------------------------------------------------------------

class Creature:
    def __init__(self):
        self.identity = IdentityCore()
        self.stm = STMOrgan()
        self.llevels = LLevelOrgan()
        self.storm = StormOrgan()
        self.mood = MoodOrgan()
        self.world = WorldOrgan()
        self.ideas = IdeaOrgan()
        self.story = StoryOrgan()
        self.math_core = MathBlockForceCore()

    def tick(self):
        self.storm.tick()
        self.mood.tick()
        self.world.tick()
        self.story.generate(self.mood, self.storm, self.ideas)
