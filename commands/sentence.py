from viewer.SentenceViewer import SentenceViewer
from organs.StructureForceEngine import StructureForceEngine
from organs.StructureScoreEngine import StructureScoreEngine
from organs.GrowthOrgan import GrowthOrgan

def run(creature):
    viewer = SentenceViewer()
    force_engine = StructureForceEngine(creature.story_modifiers)
    score_engine = StructureScoreEngine()
    growth_organ = GrowthOrgan()

    # 1. generate structure attempt
    structure_attempt = creature.generate_structure_attempt()

    # 2. compute forces
    force_output = force_engine.compute_structure_forces(
        structure_attempt["subject"],
        structure_attempt["verb"],
        structure_attempt["object"],
        structure_attempt["modifier"],
        creature.word_data,
        creature.get_dominant_story_type()
    )

    # 3. compute score
    score = score_engine.compute_score(
        force_output["force_values"],
        force_output["final_weights"]
    )
    classification = score_engine.classify_score(score)

    score_output = {
        "score": score,
        "classification": classification
    }

    # 4. apply growth
    growth_output = growth_organ.apply_growth(
        structure_attempt,
        score_output,
        force_output
    )

    # 5. display viewer
    viewer.display(structure_attempt, force_output, score_output, growth_output)
