import os

REACTIONS_FOLDER = os.path.expanduser("~/critter/reactions_uploads")

def load_reactions():
    reactions = []

    if not os.path.exists(REACTIONS_FOLDER):
        os.makedirs(REACTIONS_FOLDER)

    for filename in os.listdir(REACTIONS_FOLDER):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(REACTIONS_FOLDER, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        reactions.append(line)
        except Exception:
            continue

    return reactions

if __
