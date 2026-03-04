# organs/casino_viewer.py

class CasinoViewer:
    def __init__(self):
        self.force_icons = {
            "spark": "⚡",
            "drift": "🌬️",
            "echo": "🔊",
            "chaos": "🌀",
            "clarity": "🔍",
            "memory": "🧠",
            "pressure": "💢",
        }

    def show_spin(self, spin):
        reels = spin["reels"]
        rarity = spin["rarity"]
        pull_size = spin["pull_size"]
        combo = spin["combo"]
        jackpot = spin["jackpot"]
        packet = spin["packet"]
        loot = spin["loot"]

        color = rarity["color"]
        label = rarity["label"]
        name = rarity["name"].upper()

        print("\n🎰✨ SEMANTIC SPIN! ✨🎰\n")
        print(f"{color} {name} — {label} Pull")
        print(f"WORD PULL: {color} {pull_size} words")

        if combo:
            if combo["type"] == "combo":
                print(f"COMBO: 🟩 {combo['force']} x2 → +2 words")
            else:
                print(f"JACKPOT: 🟨✨ {combo['force']} x3 → Rarity Upgraded! ✨🟨")

        print("\nReels:")
        for r in reels:
            print(f"  {self.force_icons[r]} {r}")

        print("\nForce Packet:")
        for f, v in packet.items():
            print(f"  {self.force_icons[f]} {f}: {v}")

        print("\nLoot:")
        for word, force in loot:
            print(f"  {color} • {word}")

        print()
