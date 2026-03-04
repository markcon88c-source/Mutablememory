# ============================================================
#  SYSTEM INTEGRATOR – v1.0 (for Mark’s real creature)
#  Reads every organ in main.py and produces a unified snapshot
# ============================================================

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class SystemSnapshot:
    heartbeat: int
    pressure: Dict[str, Any]
    calm_pressure: Dict[str, Any]
    identity: Dict[str, Any]
    heart: Dict[str, Any]
    birth_forces: Dict[str, Any]
    stm: Dict[str, Any]
    llevels: Dict[str, Any]
    world: Dict[str, Any]
    story: Dict[str, Any]
    sentence: Dict[str, Any]
    mathblocks: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    cathedral: Dict[str, Any]


class SystemIntegrator:

    def __init__(self, creature):
        self.c = creature

    # ---------------------------------------------------------
    # MAIN SNAPSHOT
    # ---------------------------------------------------------
    def snapshot(self) -> SystemSnapshot:
        c = self.c

        # Pressure
        pressure_data = {
            "raw": c.pressure_core.current_pressure,
            "calm": c.calm_pressure.last_value,
        }

        # Identity (NameHeart + Factory)
        identity_data = {
            "last_packet": c.last_heart_packet,
            "last_character": c.last_character,
        }

        # Birth Forces
        birth_data = c.birth_forces.export_state()

        # STM (11 levels)
        stm_data = {
            f"L{i+1}": list(c.stm.levels[i])
            for i in range(len(c.stm.levels))
        }

        # L-Levels
        llevel_data = dict(c.l_levels.levels)

        # World
        world_data = {
            "active_world": c.world.active_world,
            "pressure": c.world.world_pressure,
            "gremlin": c.world.gremlin_pressure,
            "ideas": list(c.world.idea_history),
        }

        # Story
        story_data = {
            "sentence": c.story_viewer.last_sentence,
            "tone": c.story_viewer.last_tone,
            "ascendance": c.story_metrics.ascendance_state,
        }

        # Sentence Builder
        sentence_data = {
            "last_sentence": c.sentence_builder.last_sentence,
            "words": c.sentence_builder.last_words,
        }

        # Math Blocks
        mathblock_data = []
        for block in c.mathblocks.blocks.values():
            mathblock_data.append({
                "id": block.block_id,
                "word": block.word,
                "level": block.level,
                "micro_gate": block.micro_gate,
                "ascended": block.ascended,
                "canon": block.canon,
                "forces": block.forces.as_dict() if block.forces else {},
            })

        # Story Metrics
        metrics_data = {
            "spark": c.story_metrics.spark,
            "drift": c.story_metrics.drift,
            "echo": c.story_metrics.echo,
            "chaos": c.story_metrics.chaos,
            "clarity": c.story_metrics.clarity,
            "memory": c.story_metrics.memory,
            "pressure": c.story_metrics.pressure,
        }

        # Cathedral
        cathedral_data = {
            "active_gate": c.cathedral.active_gate,
            "birth_queue": list(c.birth_queue),
            "active_birth_character": c.active_birth_character,
        }

        return SystemSnapshot(
            heartbeat=c.heartbeat_count,
            pressure=pressure_data,
            calm_pressure={"value": c.calm_pressure.last_value},
            identity=identity_data,
            heart={"packet": c.last_heart_packet},
            birth_forces=birth_data,
            stm=stm_data,
            llevels=llevel_data,
            world=world_data,
            story=story_data,
            sentence=sentence_data,
            mathblocks=mathblock_data,
            metrics=metrics_data,
            cathedral=cathedral_data,
        )
