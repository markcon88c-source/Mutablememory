# organs/receiving_room_organ.py

import time


class ReceivingRoomOrgan:
    """
    Stores characters who have passed through the Cathedral Chamber.
    Each entry contains:
      - name
      - force score
      - timestamp
    This is the lineage archive of ascended identities.
    """

    def __init__(self, creature):
        self.creature = creature
        self.entries = []   # list of dicts

    # -----------------------------------------------------
    # RECEIVE A CHARACTER FROM THE CATHEDRAL CHAMBER
    # -----------------------------------------------------
    def receive(self, character_packet):
        if not character_packet:
            return

        entry = {
            "name": character_packet.get("full_name", "???"),
            "force_score": character_packet.get("force_score", 0.0),
            "time": time.time()
        }

        self.entries.append(entry)

    # -----------------------------------------------------
    # GET LAST N ENTRIES
    # -----------------------------------------------------
    def last(self, n=10):
        return self.entries[-n:]

    # -----------------------------------------------------
    # GET FULL ARCHIVE
    # -----------------------------------------------------
    def all(self):
        return list(self.entries)
