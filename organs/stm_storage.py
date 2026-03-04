# organs/stm_storage.py
# Daily STM storage organ (JSON, one file per day)

import os
import json
import datetime
from typing import Any, Dict, List, Optional


def _today_str() -> str:
    return datetime.date.today().isoformat()


class STMStorage:
    """
    File-backed STM storage.

    - Root dir: /storage/emulated/0/MutableMemory/stm/
    - One JSON file per day: day_YYYY-MM-DD.json
    - Tracks:
        • words (with forces + optional mathblock)
        • packets
        • sentences (with meta)
        • drift snapshots
        • pressure snapshots
    """

    def __init__(self, root_dir: Optional[str] = None):
        # Default STM root
        if root_dir is None:
            # You can adjust this if your base path differs
            base = "/storage/emulated/0/MutableMemory"
            self.root_dir = os.path.join(base, "stm")
        else:
            self.root_dir = root_dir

        os.makedirs(self.root_dir, exist_ok=True)

        self.index_path = os.path.join(self.root_dir, "index.json")
        self.current_date = _today_str()
        self.current_file = self._day_path(self.current_date)

        # In-memory buffers for the current day
        self.data: Dict[str, Any] = {
            "date": self.current_date,
            "words": [],
            "packets": [],
            "sentences": [],
            "drift": [],
            "pressures": [],
            "meta": {
                "total_words": 0,
                "total_sentences": 0,
                "avg_drift": 0.0,
                "avg_alert": 0.0,
            },
        }

        # Try to load existing index + day file
        self._load_index()
        self._load_day()

    # ---------------------------------------------------------
    # PATH HELPERS
    # ---------------------------------------------------------
    def _day_path(self, date_str: str) -> str:
        return os.path.join(self.root_dir, f"day_{date_str}.json")

    # ---------------------------------------------------------
    # INDEX HANDLING
    # ---------------------------------------------------------
    def _load_index(self):
        if not os.path.exists(self.index_path):
            self._save_index()
            return

        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                idx = json.load(f)
            self.current_date = idx.get("current_date", _today_str())
            self.current_file = self._day_path(self.current_date)
        except Exception:
            # If index is corrupted, reset
            self.current_date = _today_str()
            self.current_file = self._day_path(self.current_date)
            self._save_index()

    def _save_index(self):
        idx = {
            "current_date": self.current_date,
            "current_file": os.path.basename(self.current_file),
        }
        tmp_path = self.index_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(idx, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.index_path)

    # ---------------------------------------------------------
    # DAY FILE HANDLING
    # ---------------------------------------------------------
    def _load_day(self):
        if not os.path.exists(self.current_file):
            self._save_day()
            return

        try:
            with open(self.current_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception:
            # If corrupted, start fresh for this day
            self.data = {
                "date": self.current_date,
                "words": [],
                "packets": [],
                "sentences": [],
                "drift": [],
                "pressures": [],
                "meta": {
                    "total_words": 0,
                    "total_sentences": 0,
                    "avg_drift": 0.0,
                    "avg_alert": 0.0,
                },
            }
            self._save_day()

    def _save_day(self):
        tmp_path = self.current_file + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.current_file)

    # ---------------------------------------------------------
    # ROLLOVER (NEW DAY)
    # ---------------------------------------------------------
    def _rollover_if_needed(self):
        today = _today_str()
        if today == self.current_date:
            return

        # Save old day
        self._save_day()

        # Start new day
        self.current_date = today
        self.current_file = self._day_path(self.current_date)
        self.data = {
            "date": self.current_date,
            "words": [],
            "packets": [],
            "sentences": [],
            "drift": [],
            "pressures": [],
            "meta": {
                "total_words": 0,
                "total_sentences": 0,
                "avg_drift": 0.0,
                "avg_alert": 0.0,
            },
        }
        self._save_day()
        self._save_index()

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def tick(self):
        """
        Call this once per heartbeat.
        It will:
          - rollover to a new day if needed
          - (later) handle periodic pruning/compaction
        """
        self._rollover_if_needed()

    def append_word(self, word: str, forces: Dict[str, float], mathblock: Optional[Dict[str, Any]] = None):
        """
        Store a word that entered vocabulary from the reservoir.
        """
        self._rollover_if_needed()

        entry = {
            "word": word,
            "forces": forces,
        }
        if mathblock is not None:
            entry["mathblock"] = mathblock

        self.data["words"].append(entry)
        self.data["meta"]["total_words"] += 1
        self._save_day()

    def append_packets(self, packets: List[Dict[str, Any]]):
        """
        Store raw packets for this heartbeat / sentence build.
        """
        self._rollover_if_needed()

        # We store a shallow copy to avoid later mutation surprises
        self.data["packets"].append(packets)
        self._save_day()

    def append_sentence(self, sentence: str, meta: Dict[str, Any]):
        """
        Store a sentence and its meta (forces, drift, alert, etc.).
        """
        self._rollover_if_needed()

        entry = {
            "sentence": sentence,
            "meta": meta,
        }
        self.data["sentences"].append(entry)
        self.data["meta"]["total_sentences"] += 1

        # Update simple running averages if present
        drift_val = meta.get("drift_metrics", {}).get("drift", None)
        alert_val = meta.get("alert_pressure", {}).get("total", None)

        if drift_val is not None:
            m = self.data["meta"]
            n = max(1, m["total_sentences"])
            m["avg_drift"] = (m["avg_drift"] * (n - 1) + float(drift_val)) / n

        if alert_val is not None:
            m = self.data["meta"]
            n = max(1, m["total_sentences"])
            m["avg_alert"] = (m["avg_alert"] * (n - 1) + float(alert_val)) / n

        self._save_day()

    def append_drift_snapshot(self, drift_value: float):
        """
        Store a drift intensity snapshot.
        """
        self._rollover_if_needed()
        self.data["drift"].append(float(drift_value))
        self._save_day()

    def append_pressure_snapshot(self, pressures: Dict[str, float]):
        """
        Store a pressure ecology snapshot.
        """
        self._rollover_if_needed()
        self.data["pressures"].append(pressures)
        self._save_day()

    def get_summary(self) -> Dict[str, Any]:
        """
        Return a lightweight summary of today's STM.
        """
        self._rollover_if_needed()
        return {
            "date": self.data.get("date"),
            "total_words": self.data["meta"]["total_words"],
            "total_sentences": self.data["meta"]["total_sentences"],
            "avg_drift": self.data["meta"]["avg_drift"],
            "avg_alert": self.data["meta"]["avg_alert"],
        }


class STMOrgan:
    """
    Thin wrapper so the creature can treat this as an organ.
    """

    def __init__(self, creature=None, root_dir: Optional[str] = None):
        self.creature = creature
        self.storage = STMStorage(root_dir=root_dir)

    def tick(self):
        self.storage.tick()

    def append_word(self, word: str, forces: Dict[str, float], mathblock: Optional[Dict[str, Any]] = None):
        self.storage.append_word(word, forces, mathblock)

    def append_packets(self, packets: List[Dict[str, Any]]):
        self.storage.append_packets(packets)

    def append_sentence(self, sentence: str, meta: Dict[str, Any]):
        self.storage.append_sentence(sentence, meta)

    def append_drift_snapshot(self, drift_value: float):
        self.storage.append_drift_snapshot(drift_value)

    def append_pressure_snapshot(self, pressures: Dict[str, float]):
        self.storage.append_pressure_snapshot(pressures)

    def get_summary(self) -> Dict[str, Any]:
        return self.storage.get_summary()
