import time

class ReceivingRoomViewer:
    def __init__(self, creature):
        self.creature = creature

    # -----------------------------------
    # MOVIE CREDIT STYLE SCROLL
    # -----------------------------------
    # Slower scroll: 0.20 seconds per line
    def scroll_block(self, lines, delay=0.20):
        for line in lines:
            print(line)
            time.sleep(delay)

    def bar(self, value, length=10, emoji="🟦"):
        filled = int(value * length)
        empty = length - filled
        return emoji * filled + "▫️" * empty

    # -----------------------------------
    # DIAGNOSTICS VIEW
    # -----------------------------------
    def show_diagnostics(self):
        room = self.creature.birth_archive

        # STATIC HEADER (no scroll)
        print("╔" + "═" * 46 + "╗")
        print("║{:^46}║".format("RECEIVING ROOM — DIAGNOSTICS"))
        print("╚" + "═" * 46 + "╝\n")

        # STATIC CAST LIST (no scroll)
        if not room:
            print("No characters have arrived yet.")
            return

        print("🧍 Characters Present:\n")
        for i, c in enumerate(room, 1):
            name = c.get("full_name", "Unknown")
            block = c.get("block_id", "?")
            score = round(c.get("force_score", 0.0), 2)

            print(f"  {i}. {name}")
            print(f"     🔢 Block: {block}")
            print(f"     ✨ Force Score: {score}\n")

        # -----------------------------------
        # SCROLLING DIAGNOSTIC CONTENT
        # -----------------------------------
        lines = []
        lines.append("📊 Diagnostic Summary:")
        lines.append("")

        for c in room:
            name = c.get("full_name", "Unknown")
            block = c.get("block_id", "?")
            score = round(c.get("force_score", 0.0), 2)

            lines.append(f"{name} — Block {block}, Score {score}")
            lines.append("")

        self.scroll_block(lines, delay=0.20)

    # -----------------------------------
    # PAIR NARRATION
    # -----------------------------------
    def pair_narration(self, A, B, affinity, tension, curiosity, dominance, resonance):
        lines = []

        if affinity > 0.7:
            lines.append(f"{A} and {B} feel an easy warmth between them.")
        elif tension > 0.6:
            lines.append(f"There is a sharp edge in the air between {A} and {B}.")
        elif curiosity > 0.6:
            lines.append(f"{A} and {B} study each other with cautious curiosity.")
        else:
            lines.append(f"{A} and {B} acknowledge each other quietly.")

        if dominance > 0.6:
            lines.append(f"{A} subtly leads the interaction.")
        elif dominance < 0.4:
            lines.append(f"{B} takes the social lead.")

        if resonance:
            lines.append(f"A faint mythic resonance hums between them.")

        return " ".join(lines)

    # -----------------------------------
    # TRIAD NARRATION
    # -----------------------------------
    def triad_narration(self, A, B, C):
        a = A.get("block_id", 0)
        b = B.get("block_id", 0)
        c = C.get("block_id", 0)

        diffs = [abs(a-b), abs(a-c), abs(b-c)]
        avg_affinity = 1 - (sum(diffs) / 3) / 9
        max_tension = max(diffs) / 9

        scores = {
            A["full_name"]: A.get("force_score", 1),
            B["full_name"]: B.get("force_score", 1),
            C["full_name"]: C.get("force_score", 1),
        }
        leader = max(scores, key=scores.get)

        if avg_affinity > 0.7:
            line = f"{A['full_name']}, {B['full_name']}, and {C['full_name']} form a harmonious triad."
        elif max_tension > 0.6:
            line = f"Tension ripples through the triad of {A['full_name']}, {B['full_name']}, and {C['full_name']}."
        else:
            line = f"{A['full_name']}, {B['full_name']}, and {C['full_name']} share a tentative, neutral connection."

        line += f" {leader} naturally becomes the center of the group."

        return line

    # -----------------------------------
    # INTERACTIONS VIEW
    # -----------------------------------
    def show_interactions(self):
        room = self.creature.birth_archive

        # STATIC HEADER
        print("╔" + "═" * 46 + "╗")
        print("║{:^46}║".format("RECEIVING ROOM — INTERACTIONS"))
        print("╚" + "═" * 46 + "╝\n")

        # STATIC CAST LIST
        if not room:
            print("No characters have arrived yet.")
            return

        print("🧍 Characters Present:\n")
        for i, c in enumerate(room, 1):
            name = c.get("full_name", "Unknown")
            block = c.get("block_id", "?")
            score = round(c.get("force_score", 0.0), 2)

            print(f"  {i}. {name}")
            print(f"     🔢 Block: {block}")
            print(f"     ✨ Force Score: {score}\n")

        # -----------------------------------
        # SCROLLING INTERACTION CONTENT
        # -----------------------------------
        lines = []
        lines.append("🤝 Pair Interactions:")
        lines.append("")

        for i in range(len(room)):
            for j in range(i + 1, len(room)):
                A = room[i]
                B = room[j]

                a = A.get("block_id", 0)
                b = B.get("block_id", 0)

                affinity = 1 - abs(a - b) / 9
                tension = abs(a - b) / 9
                curiosity = 1 - abs(affinity - tension)

                scoreA = A.get("force_score", 1)
                scoreB = B.get("force_score", 1)
                dominance = scoreA / (scoreA + scoreB)

                resonance = (a + b in (10, 11))

                lines.append(f"🔷 {A['full_name']} ↔ {B['full_name']}")
                lines.append(f"   💙 Affinity:   {self.bar(affinity, emoji='💙')}  {affinity:.2f}")
                lines.append(f"   ❤️ Tension:    {self.bar(tension, emoji='❤️')}  {tension:.2f}")
                lines.append(f"   💛 Curiosity:  {self.bar(curiosity, emoji='💛')}  {curiosity:.2f}")
                lines.append("   🗣️ " + self.pair_narration(
                    A['full_name'], B['full_name'],
                    affinity, tension, curiosity,
                    dominance, resonance
                ))
                lines.append("")

        if len(room) >= 3:
            lines.append("🔺 Triad Dynamics:")
            lines.append("")
            for i in range(len(room)):
                for j in range(i+1, len(room)):
                    for k in range(j+1, len(room)):
                        A, B, C = room[i], room[j], room[k]
                        lines.append("   " + self.triad_narration(A, B, C))
                        lines.append("")

        self.scroll_block(lines, delay=0.20)
