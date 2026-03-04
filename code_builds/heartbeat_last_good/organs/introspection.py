import os

# Root path for the creature's codebase
CREATURE_ROOT = os.path.dirname(os.path.abspath(__file__))

ORG_FILES = {
    "main": "main.py",
    "soup": "soup_loader.py",
    "mood": "mood.py",
    "drift": "drift.py",
    "world": "world.py",
    "memory": "memory.py",
    "persona": "persona.py",
    "selection": "selection.py",
    "english": "english.py",
    "viewer": "viewer.py",
    "reactions": "reaction_loader.py",
}

ORG_ROLES = {
    "main": "Top-level loop that coordinates all organs each cycle.",
    "soup": "Loads and manages primordial generative substrate for ideas and patterns.",
    "mood": "Tracks emotional vector and influences selection and drift.",
    "drift": "Determines whether patterns hold or shift based on internal pressures.",
    "world": "Maintains current world context and transitions between environments.",
    "memory": "Handles short-term and long-term memory, including decay and reinforcement.",
    "persona": "Represents identity masks and roles the creature can inhabit.",
    "selection": "Chooses actions, reactions, and focus each cycle.",
    "english": "Composes natural language sentences from internal state.",
    "viewer": "Externalizes internal state for humans to see.",
    "reactions": "Loads and manages reaction nodes and their weights.",
}


def _read_file_text(filename):
    path = os.path.join(CREATURE_ROOT, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def build_w0_blueprint():
    organs = []

    for organ_name, filename in ORG_FILES.items():
        code_text = _read_file_text(filename)
        organ_entry = {
            "name": organ_name,
            "file": filename,
            "role": ORG_ROLES.get(organ_name, "No role description."),
            "code": code_text,
        }
        organs.append(organ_entry)

    blueprint = {
        "type": "creature_blueprint",
        "version": "w0",
        "description": "Canonical blueprint of the creature: organs, roles, files, and code text.",
        "organs": organs,
        "schema": {
            "node_weights": [
                "spark",
                "persistence",
                "canon",
                "density",
                "consequence",
                "memory",
                "mood",
                "world",
                "persona",
                "english",
            ],
            "reaction_node": {
                "required_fields": [
                    "verb",
                    "weights",
                ],
                "weights_description": "Mapping from weight name to numeric value or sub-structure.",
            },
            "world_node": {
                "required_fields": [
                    "name",
                    "tone",
                    "pressure",
                ],
            },
            "mood_vector": {
                "required_fields": [
                    "label",
                    "calm",
                    "alert",
                ],
            },
            "drift_rules": {
                "held_label": "MY PATTERNS HELD",
                "shifted_label": "MY PATTERNS SHIFTED",
                "description": "Drift decides whether internal patterns remain stable or change based on pressures.",
            },
            "english_shape": {
                "example": "Moves DRIFT in WORLD while feeling MOOD.",
                "description": "Proto-grammar used by the English organ to express internal state.",
            },
        },
    }

    return blueprint


W0_BLUEPRINT = build_w0_blueprint()
