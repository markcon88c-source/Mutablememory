import os
import random
import time

class FieldPacket:
    def __init__(self, raw_sentence, drift, climate, motif_pressure, force_echoes, residue, timestamp):
        self.raw_sentence = raw_sentence
        self.drift = drift
        self.climate = climate
        self.motif_pressure = motif_pressure
        self.force_echoes = force_echoes
        self.residue = residue
        self.timestamp = timestamp

class EnglishField:
    def __init__(self, base_path):
        self.base_path = base_path

        self.general_path = os.path.join(base_path, "English/general/general.txt")
        self.story_path = os.path.join(base_path, "English/story/story.txt")

        self.general_samples = []
        self.story_samples = []
        self.all_samples = []

        self.last_sentences = []
        self.max_memory = 10

        self.climate_state = {
            "stability": 0.5,
            "drift": 0.5,
            "resonance": 0.5,
            "memory": 0.5,
            "chaos": 0.5
        }

        self.motif_pressure = {
            "object": 0.5,
            "motion": 0.5,
            "emotion": 0.5,
            "space": 0.5,
            "time": 0.5
        }

        self.story_type_drift = {
            "everyday": 0.5,
            "story": 0.5,
            "dream": 0.5,
            "symbol": 0.5,
            "mythic": 0.5
        }

        self.force_echoes = {
            "soft": 0.5,
            "sharp": 0.5,
            "warm": 0.5,
            "cool": 0.5,
            "neutral": 0.5
        }

        self.residue = {
            "last_word": "",
            "length": 0,
            "punctuation": ""
        }

        self.load_all()

    def load_file(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        return lines

    def load_all(self):
        self.general_samples = self.load_file(self.general_path)
        self.story_samples = self.load_file(self.story_path)
        self.all_samples = self.general_samples + self.story_samples

    def pick_sentence(self):
        if not self.all_samples:
            return ""
        return random.choice(self.all_samples)

    def update_climate(self):
        for k in self.climate_state:
            delta = random.uniform(-0.02, 0.02)
            self.climate_state[k] = max(0.0, min(1.0, self.climate_state[k] + delta))

    def update_motif_pressure(self, sentence):
        length = len(sentence.split())
        if length < 6:
            self.motif_pressure["object"] += 0.01
        elif length < 12:
            self.motif_pressure["motion"] += 0.01
        else:
            self.motif_pressure["space"] += 0.01

        for k in self.motif_pressure:
            self.motif_pressure[k] = max(0.0, min(1.0, self.motif_pressure[k]))

    def update_story_drift(self, sentence):
        if "he " in sentence.lower() or "she " in sentence.lower():
            self.story_type_drift["everyday"] += 0.01
        if "window" in sentence.lower() or "street" in sentence.lower():
            self.story_type_drift["story"] += 0.01
        if "quiet" in sentence.lower() or "soft" in sentence.lower():
            self.story_type_drift["dream"] += 0.01

        for k in self.story_type_drift:
            self.story_type_drift[k] = max(0.0, min(1.0, self.story_type_drift[k]))

    def update_force_echoes(self, sentence):
        if "soft" in sentence.lower():
            self.force_echoes["soft"] += 0.02
        if "cold" in sentence.lower() or "cool" in sentence.lower():
            self.force_echoes["cool"] += 0.02
        if "warm" in sentence.lower():
            self.force_echoes["warm"] += 0.02

        for k in self.force_echoes:
            self.force_echoes[k] = max(0.0, min(1.0, self.force_echoes[k]))

    def update_residue(self, sentence):
        words = sentence.split()
        if words:
            self.residue["last_word"] = words[-1]
            self.residue["length"] = len(words)
            self.residue["punctuation"] = sentence[-1] if sentence[-1] in ".!?" else ""

    def update_memory(self, sentence):
        self.last_sentences.append(sentence)
        if len(self.last_sentences) > self.max_memory:
            self.last_sentences.pop(0)

    def produce(self):
        sentence = self.pick_sentence()
        self.update_climate()
        self.update_motif_pressure(sentence)
        self.update_story_drift(sentence)
        self.update_force_echoes(sentence)
        self.update_residue(sentence)
        self.update_memory(sentence)

        packet = FieldPacket(
            raw_sentence=sentence,
            drift=self.story_type_drift.copy(),
            climate=self.climate_state.copy(),
            motif_pressure=self.motif_pressure.copy(),
            force_echoes=self.force_echoes.copy(),
            residue=self.residue.copy(),
            timestamp=time.time()
        )

        return packet

    def export_state(self):
        return {
            "last_sentences": list(self.last_sentences),
            "climate": dict(self.climate_state),
            "drift": dict(self.story_type_drift),
            "motif_pressure": dict(self.motif_pressure),
            "force_echoes": dict(self.force_echoes),
            "residue": dict(self.residue)
        }
