def sentence_packet(text):
    return {"type": "sentence", "sentence": text}

def narrative_packet(text):
    return {"type": "narrative", "narrative": text}
def character_birth_packet(payload):
    return {
        "type": "birth",
        "payload": payload,
        "source": "character_birth",
    }

def character_forces_packet(payload):
    return {
        "type": "character_forces",
        "payload": payload,
        "source": "character_sheet_to_forces",
    }

def identity_packet(payload):
    return {
        "type": "identity",
        "payload": payload,
        "source": "identity_organ",
    }

def pressure_packet(payload):
    return {
        "type": "pressure",
        "payload": payload,
        "source": "pressure_organ",
    }
