# reason_atlas_generator.py
# Generates reason_atlas.txt with full broken-line protection

import random
import json

# ------------------------------------------------------------
# 1. REASON POOLS
# ------------------------------------------------------------

REASONS = {
    "spark": {
        "success": [
            "Ignition Burst", "Emotional Voltage", "Novelty Flash",
            "Creative Surge", "Mythic Spark", "Symbolic Charge",
            "Friction Ignition"
        ],
        "failure": [
            "Spark Fizzle", "Emotional Flatline", "Stale Entry",
            "Cold Ember", "Symbolic Weakness", "Dampened Spark",
            "Spark Suppression"
        ]
    },
    "drift": {
        "success": [
            "Directional Alignment", "Momentum Match", "Trajectory Harmony",
            "Vector Sync", "Path Resonance", "Forward Drift",
            "Arc Continuation"
        ],
        "failure": [
            "Drift Misalignment", "Momentum Clash", "Trajectory Break",
            "Vector Opposition", "Path Disruption", "Arc Fracture",
            "Flow Reversal"
        ]
    },
    "echo": {
        "success": [
            "Harmonic Echo", "Semantic Rhyme", "Emotional Echo",
            "Conceptual Reflection", "Pattern Continuation",
            "Chord Formation", "Resonant Return"
        ],
        "failure": [
            "Echo Dissonance", "Semantic Break", "Emotional Dissonance",
            "Pattern Violation", "Chord Collapse", "Resonance Failure",
            "Echo Drift"
        ]
    },
    "chaos": {
        "success": [
            "Chaos Jackpot", "Entropy Surge", "Gremlin Blessing",
            "Disruption Advantage", "Wild Card Entry",
            "Lucky Break", "Chaotic Favor"
        ],
        "failure": [
            "Chaos Interference", "Entropy Drain", "Gremlin Trick",
            "Noise Overload", "Wild Card Collapse",
            "Chaotic Sabotage", "Entropy Spike"
        ]
    },
    "clarity": {
        "success": [
            "Signal Dominance", "Precision Strike", "Conceptual Sharpness",
            "Narrative Focus", "Symbolic Precision",
            "Clarity Beam", "Definition Surge"
        ],
        "failure": [
            "Clarity Collapse", "Signal Loss", "Conceptual Blur",
            "Narrative Fog", "Symbolic Weakness",
            "Definition Failure", "Signal Scatter"
        ]
    },
    "memory": {
        "success": [
            "Memory Anchor", "Return Weight", "Familiar Echo",
            "Reinforced Pattern", "Archetypal Recall",
            "Deep Memory Pull", "Mnemonic Surge"
        ],
        "failure": [
            "Memory Rejection", "Weak Recall", "Pattern Break",
            "Archetypal Drift", "Faded Trace",
            "Mnemonic Failure", "Recall Collapse"
        ]
    },
    "pressure": {
        "success": [
            "Pressure Breakthrough", "Force Convergence",
            "Threshold Overrun", "Dominance Spike",
            "Critical Mass", "Force Alignment",
            "Pressure Surge"
        ],
        "failure": [
            "Pressure Shortfall", "Force Fragmentation",
            "Threshold Miss", "Dominance Failure",
            "Critical Weakness", "Force Collapse",
            "Pressure Leak"
        ]
    }
}

# ------------------------------------------------------------
# 2. RANDOM MATHBLOCK
# ------------------------------------------------------------

def random_mathblock():
    return {
        "spark": round(random.uniform(-1, 1), 2),
        "drift": round(random.uniform(-1, 1), 2),
        "echo": round(random.uniform(-1, 1), 2),
        "chaos": round(random.uniform(-1, 1), 2),
        "clarity": round(random.uniform(-1, 1), 2),
        "memory": round(random.uniform(-1, 1), 2),
        "pressure": "auto"
    }

# ------------------------------------------------------------
# 3. BROKEN LINE GUARD
# ------------------------------------------------------------

def safe_write(f, text):
    """Writes only full, unbroken lines."""
    if "\n" in text:
        # If text contains embedded newlines, reject it
        return
    if not text.strip():
        return
    f.write(text + "\n")

# ------------------------------------------------------------
# 4. GENERATOR
# ------------------------------------------------------------

def generate_reason_atlas(words):
    with open("reason_atlas.txt", "w") as f:
        for word in words:
            safe_write(f, "============================================================")
            safe_write(f, f"WORD: {word}")
            safe_write(f, "TYPE: unknown")
            safe_write(f, "LEVEL: L1-00")
            safe_write(f, "")

            for force, groups in REASONS.items():

                # Success
                safe_write(f, f"{force.upper()} (Success):")
                for reason in groups["success"]:
                    block = json.dumps(random_mathblock())
                    safe_write(f, f"  ✔ {reason}  {block}")
                safe_write(f, "")

                # Failure
                safe_write(f, f"{force.upper()} (Failure):")
                for reason in groups["failure"]:
                    block = json.dumps(random_mathblock())
                    safe_write(f, f"  ✖ {reason}  {block}")
                safe_write(f, "")

            safe_write(f, "============================================================")
            safe_write(f, "")

# ------------------------------------------------------------
# 5. LOAD WORD LIST
# ------------------------------------------------------------

def load_words(path="vocabulary/reservoir.txt"):
    words = []
    with open(path, "r") as f:
        for line in f:
            w = line.strip()
            if w:
                words.append(w)
    return words

# ------------------------------------------------------------
# 6. MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    words = load_words()
    generate_reason_atlas(words)
    print("reason_atlas.txt generated successfully.")
