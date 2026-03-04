# organs/casino_force_core.py
import random

class CasinoForceCore:
    """
    Semantic gacha casino:
    - Spins 3 reels of forces
    - Determines rarity
    - Computes word pull size
    - Applies combo/jackpot bonuses
    - Generates force-flavored word loot
    """

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

        # Forces
        self.forces = [
            "spark",
            "drift",
            "echo",
            "chaos",
            "clarity",
            "memory",
            "pressure",
        ]

        # Rarity table: (name, drop_rate, min_words, max_words, color_emoji, label)
        self.rarity_table = [
            ("common",    0.70, 1,  4,  "🟦", "Whisper"),
            ("uncommon",  0.20, 3,  8,  "🟩", "Echo"),
            ("rare",      0.08, 6, 14,  "🟪", "Burst"),
            ("legendary", 0.02, 10, 25, "🟨✨", "Mythic"),
        ]

        # Simple force-flavored word pools
        self.word_pools = {
            "spark": [
                "ignite", "start", "spark", "kickoff", "trigger", "flash",
            ],
            "drift": [
                "drift", "slide", "wander", "float", "glide", "slip",
            ],
            "echo": [
                "echo", "resonate", "repeat", "reverb", "callback", "trace",
            ],
            "chaos": [
                "fracture", "tilt", "rupture", "scatter", "glitch", "spiral",
            ],
            "clarity": [
                "define", "sharpen", "refine", "isolate", "focus", "distill",
            ],
            "memory": [
                "recall", "whisper", "imprint", "remnant", "trace", "keepsake",
            ],
            "pressure": [
                "strain", "tension", "surge", "crush", "pulse", "spike",
            ],
        }

    # ---------- core helpers ----------

    def spin_reel(self):
        return self.rng.choice(self.forces)

    def choose_rarity(self):
        roll = self.rng.random()
        cumulative = 0.0
        for name, prob, min_w, max_w, color, label in self.rarity_table:
            cumulative += prob
            if roll <= cumulative:
                return {
                    "name": name,
                    "min_words": min_w,
                    "max_words": max_w,
                    "color": color,
                    "label": label,
                }
        # Fallback (should not happen)
        name, prob, min_w, max_w, color, label = self.rarity_table[-1]
        return {
            "name": name,
            "min_words": min_w,
            "max_words": max_w,
            "color": color,
            "label": label,
        }

    def bump_rarity(self, rarity_info):
        # Upgrade rarity one tier if possible
        names = [r[0] for r in self.rarity_table]
        idx = names.index(rarity_info["name"])
        if idx < len(self.rarity_table) - 1:
            name, prob, min_w, max_w, color, label = self.rarity_table[idx + 1]
            return {
                "name": name,
                "min_words": min_w,
                "max_words": max_w,
                "color": color,
                "label": label,
            }
        return rarity_info

    def random_word_count(self, rarity_info):
        return self.rng.randint(rarity_info["min_words"], rarity_info["max_words"])

    # ---------- main spin ----------

    def spin(self):
        """
        Returns a dict with:
        - reels: list of 3 forces
        - rarity: {name, min_words, max_words, color, label}
        - pull_size: int
        - combo: None or dict
        - jackpot: bool
        - packet: {force: value}
        - loot: list of (word, force)
        """
        # Spin reels
        reel1 = self.spin_reel()
        reel2 = self.spin_reel()
        reel3 = self.spin_reel()
        reels = [reel1, reel2, reel3]

        # Count occurrences
        counts = {}
        for r in reels:
            counts[r] = counts.get(r, 0) + 1

        # Base force packet
        packet = {f: 0 for f in self.forces}
        for force, count in counts.items():
            packet[force] = self.rng.randint(1, 4) * count

        # Base rarity
        rarity = self.choose_rarity()

        combo = None
        jackpot = False
        combo_bonus_words = 0

        # 2-match combo
        if 2 in counts.values():
            combo = {
                "type": "combo",
                "force": [f for f, c in counts.items() if c == 2][0],
            }
            combo_bonus_words += 2
            # 10% chance to bump rarity
            if self.rng.random() < 0.10:
                rarity = self.bump_rarity(rarity)

        # 3-match jackpot
        if len(counts) == 1:
            jackpot = True
            combo = {
                "type": "jackpot",
                "force": reels[0],
            }
            rarity = self.bump_rarity(rarity)
            # small extra force bonus
            packet[reels[0]] += 5

        # Word pull size
        pull_size = self.random_word_count(rarity) + combo_bonus_words

        # Generate loot words, weighted by packet values
        loot = self.generate_loot(pull_size, packet)

        return {
            "reels": reels,
            "rarity": rarity,
            "pull_size": pull_size,
            "combo": combo,
            "jackpot": jackpot,
            "packet": packet,
            "loot": loot,
        }

    def generate_loot(self, pull_size, packet):
        """
        Generate a list of (word, force) pairs.
        Forces with higher packet values are more likely to be chosen.
        """
        loot = []
        total = sum(max(v, 0) for v in packet.values())
        if total <= 0:
            # fallback: uniform over forces
            weights = {f: 1 for f in self.forces}
            total = len(self.forces)
        else:
            weights = {f: max(v, 0) for f, v in packet.items()}

        for _ in range(pull_size):
            # pick a force by weight
            roll = self.rng.uniform(0, total)
            cumulative = 0
            chosen_force = self.forces[0]
            for f in self.forces:
                cumulative += weights.get(f, 0)
                if roll <= cumulative:
                    chosen_force = f
                    break
            pool = self.word_pools.get(chosen_force, ["word"])
            word = self.rng.choice(pool)
            loot.append((word, chosen_force))

        return loot
