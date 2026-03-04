import json
import os
from organs.base_organ import BaseOrgan

class ShoreOrgan(BaseOrgan):
    """
    The ShoreOrgan is the exchange membrane between MeaningOrgan and OceanOrgan.
    It handles:
      - receiving sentences from MeaningOrgan
      - writing them to ocean_in.json
      - reading transformed sentences from ocean_out.json
      - handing them back to MeaningOrgan
    """

    def __init__(self, creature):
        super().__init__(creature)

        # file paths
        self.ocean_in_path = "ocean/ocean_in.json"
        self.ocean_out_path = "ocean/ocean_out.json"

        # ensure directory exists
        os.makedirs("ocean", exist_ok=True)

        # initialize files if missing
        if not os.path.exists(self.ocean_in_path):
            with open(self.ocean_in_path, "w") as f:
                json.dump({"sentences": []}, f)

        if not os.path.exists(self.ocean_out_path):
            with open(self.ocean_out_path, "w") as f:
                json.dump({"sentences": []}, f)

        # buffer for sentences returning from the ocean
        self.return_buffer = []

    # ---------------------------------------------------------
    # Main metabolic tick
    # ---------------------------------------------------------
    def step(self):
        """
        1. Pull new sentences from MeaningOrgan
        2. Write them to ocean_in.json
        3. Read ocean_out.json for transformed sentences
        4. Return them to MeaningOrgan
        """
        self.receive_from_meaning()
        self.write_to_ocean()
        self.read_from_ocean()
        self.return_to_meaning()

        return {
            "outgoing": self._read_json(self.ocean_in_path),
            "incoming": list(self.return_buffer),
        }

    # ---------------------------------------------------------
    # 1. Receive sentences from MeaningOrgan
    # ---------------------------------------------------------
    def receive_from_meaning(self):
        meaning = self.creature.organs.get("MeaningOrgan")
        if not meaning:
            return

        packet = meaning.get_latest_sentence()
        if packet:
            self._append_json(self.ocean_in_path, packet)

    # ---------------------------------------------------------
    # 2. Write to ocean_in.json (already done by append)
    # ---------------------------------------------------------
    def write_to_ocean(self):
        # nothing else needed here yet
        pass

    # ---------------------------------------------------------
    # 3. Read transformed sentences from ocean_out.json
    # ---------------------------------------------------------
    def read_from_ocean(self):
        data = self._read_json(self.ocean_out_path)
        if not data:
            return

        sentences = data.get("sentences", [])
        if sentences:
            self.return_buffer.extend(sentences)

        # clear ocean_out after reading
        with open(self.ocean_out_path, "w") as f:
            json.dump({"sentences": []}, f)

    # ---------------------------------------------------------
    # 4. Return sentences to MeaningOrgan
    # ---------------------------------------------------------
    def return_to_meaning(self):
        meaning = self.creature.organs.get("MeaningOrgan")
        if not meaning:
            return

        for s in self.return_buffer:
            meaning.receive_from_ocean(s)

        self.return_buffer.clear()

    # ---------------------------------------------------------
    # JSON helpers
    # ---------------------------------------------------------
    def _read_json(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}

    def _append_json(self, path, sentence):
        data = self._read_json(path)
        if "sentences" not in data:
            data["sentences"] = []
        data["sentences"].append(sentence)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
