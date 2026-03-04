import random
import time

class NameHeart:
    """
    The Naming Heart beats every N heartbeats and produces an identity packet.
    It can also mutate incoming character packets.
    """

    def __init__(self, creature, rate=5):
        self.creature = creature
        self.rate = rate
        self.counter = 0

    # -----------------------------------------------------
    # BUS LISTENER — mutate character packets
    # -----------------------------------------------------
    def handle_bus_packet(self, packet):
        channel = packet.get("channel")
        payload = packet.get("payload")

        if channel == "character":
            mutated = self.mutate_character_packet(payload)
            bus = getattr(self.creature, "bus", None)
            if bus is not None:
                bus.emit(
                    source="nameheart",
                    channel="character",
                    kind="mutated_identity",
                    payload=mutated,
                )

    # =====================================================
    # Cathedral metabolism tick
    # =====================================================
    def tick_core(self, creature):
        self.counter += 1

        # Only fire every N heartbeats
        if self.counter % self.rate != 0:
            return None

        packet = self.generate_packet()
        return {
            "source": "name_heart",
            "channel": "identity",
            "kind": "identity_seed",
            "payload": packet,
        }

    # Legacy wrapper
    def tick(self):
        return self.tick_core(self.creature)

    # -----------------------------------------------------
    # PACKET GENERATION
    # -----------------------------------------------------
    def generate_packet(self):
        first = self.generate_name()
        last = self.generate_name()
        full = f"{first} {last}"

        phoneme = self.phonemize(first)
        surname_phoneme = self.phonemize(last)
        cluster = self.make_cluster(phoneme, surname_phoneme)

        pulse = random.random()
        tone = random.random()
        force_type, force_target = self.force_profile(pulse, tone)

        origin_block_id = random.randint(1, 20)
        parent_block_ids = [random.randint(1, 20), random.randint(1, 20)]

        seed = f"{first[:2].lower()}{last[:2].lower()}"
        letters = list(cluster)
        mode = "mythic" if (pulse + tone) > 1 else "mortal"
        force = force_type
        block_id = origin_block_id

        return {
            "name": first,
            "surname": last,
            "full_name": full,
            "phoneme": phoneme,
            "surname_phoneme": surname_phoneme,
            "cluster": cluster,
            "pulse": pulse,
            "tone": tone,
            "force_type": force_type,
            "force_target": force_target,
            "origin_block_id": origin_block_id,
            "parent_block_ids": parent_block_ids,
            "seed": seed,
            "letters": letters,
            "mode": mode,
            "force": force,
            "block_id": block_id,
        }

    # -----------------------------------------------------
    # CHARACTER PACKET MUTATION
    # -----------------------------------------------------
    def mutate_character_packet(self, packet):
        name = packet.get("name", "")
        mutated = self.mutate_name(name)
        packet["name"] = mutated
        packet["letters"] = list(mutated)
        packet["full_name"] = mutated
        return packet

    # -----------------------------------------------------
    # NAME MUTATION ENGINE
    # -----------------------------------------------------
    def mutate_name(self, name):
        if not name:
            return name

        choice = random.choice([
            "letter", "syllable", "swap", "truncate", "synergy"
        ])

        if choice == "letter":
            return self.mutate_letters(name)
        elif choice == "syllable":
            return self.mutate_syllables(name)
        elif choice == "swap":
            return self.swap_halves(name)
        elif choice == "truncate":
            return self.truncate_name(name)
        else:
            return self.synergy_mutation(name)

    def mutate_letters(self, name):
        if len(name) < 2:
            return name
        idx = random.randint(0, len(name) - 1)
        letters = list(name)
        letters[idx] = random.choice("aeioulrnstdkmv")
        return "".join(letters).capitalize()

    def mutate_syllables(self, name):
        syllables = ["sha", "kra", "tha", "lor", "wen",
                     "sol", "mir", "tal", "vor", "ena"]
        new = random.choice(syllables)
        return (new + name[len(new):]).capitalize()

    def swap_halves(self, name):
        mid = len(name) // 2
        return (name[mid:] + name[:mid]).capitalize()

    def truncate_name(self, name):
        if len(name) <= 3:
            return name
        cut = random.randint(2, len(name) - 1)
        return name[:cut].capitalize()

    def synergy_mutation(self, name):
        name = self.mutate_letters(name)
        name = self.swap_halves(name)
        return self.mutate_syllables(name)

    # -----------------------------------------------------
    # NAME GENERATION
    # -----------------------------------------------------
    def generate_name(self):
        syllables = [
            "sha", "kra", "tha", "lor", "wen",
            "sol", "mir", "tal", "vor", "ena",
            "sil", "dra", "kor", "bel", "rin"
        ]
        return random.choice(syllables).capitalize() + random.choice(syllables)

    # -----------------------------------------------------
    # PHONEMES
    # -----------------------------------------------------
    def phonemize(self, name):
        return "-".join([name[i:i+2] for i in range(0, len(name), 2)])

    # -----------------------------------------------------
    # CLUSTER
    # -----------------------------------------------------
    def make_cluster(self, p1, p2):
        letters = (p1 + p2).replace("-", "")
        base = letters[:5] if len(letters) >= 5 else letters.ljust(5, "x")
        return "".join(random.choice("UAW") for _ in base)

    # -----------------------------------------------------
    # FORCE PROFILE
    # -----------------------------------------------------
    def force_profile(self, pulse, tone):
        if pulse > 0.66:
            return "spark", pulse
        elif pulse > 0.33:
            return "drift", tone
        else:
            return "echo", (pulse + tone) / 2
