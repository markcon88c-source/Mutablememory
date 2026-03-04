# organs/alert_pressure.py
# FULL AlertPressure Cathedral – unified organ, no external imports

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class AlertConfig:
    # Master weights
    w_threat_geometry: float = 1.0
    w_shadow_memory: float = 1.0
    w_storm_resonance: float = 1.0
    w_cognitive_load: float = 1.0
    w_shadow_drift: float = 1.0
    w_heartbeat_sync: float = 1.0
    w_meaning_collapse: float = 1.0
    w_chaos_gremlin: float = 1.0
    w_orientation_loss: float = 1.0
    w_emotional_volcano: float = 1.0

    # Global tuning
    base_decay: float = 0.03
    redline_threshold: float = 0.8
    spike_count_soft: int = 3
    spike_count_hard: int = 5

    # Cognitive load sweet spot
    stm_low: int = 1
    stm_high: int = 40

    # Meaning thresholds
    low_sentence_comfort: float = 0.25
    low_symbolic_pressure: float = 0.25
    low_word_strength: float = 0.25
    low_concentration: float = 0.25

    # Storm / drift thresholds
    storm_high: float = 0.6
    drift_unstable: float = 0.4
    drift_accel_high: float = 0.4

    # Chaos / gremlin
    chaos_high: float = 0.6

    # Emotional volcano
    symbolic_pressure_high: float = 0.6

    # Rhythm
    heartbeat_desync_penalty: float = 0.3


class AlertPressure:
    """
    Full cathedral organ. Creature imports this class directly.
    """

    def __init__(self, config: Optional[AlertConfig] = None):
        self.config = config or AlertConfig()
        self.current_alert: float = 0.0
        self.last_subvalues: Dict[str, float] = {}

    # ---------------- PUBLIC ENTRYPOINT ----------------

    def compute(self, metrics: Dict[str, Any]) -> float:
        """
        Creature calls this each heartbeat.
        metrics: dict of creature state; all keys optional.
        Returns alert in [0, 1].
        """

        subs = {
            "threat_geometry": self._threat_geometry(metrics),
            "shadow_memory": self._shadow_memory(metrics),
            "storm_resonance": self._storm_resonance(metrics),
            "cognitive_load": self._cognitive_load(metrics),
            "shadow_drift": self._shadow_drift(metrics),
            "heartbeat_sync": self._heartbeat_sync(metrics),
            "meaning_collapse": self._meaning_collapse(metrics),
            "chaos_gremlin": self._chaos_gremlin(metrics),
            "orientation_loss": self._orientation_loss(metrics),
            "emotional_volcano": self._emotional_volcano(metrics),
        }

        delta, spike_count = self._master_regulator(subs)

        # decay
        self.current_alert = max(0.0, self.current_alert - self.config.base_decay)

        # apply delta
        self.current_alert += delta

        # clamp
        self.current_alert = max(0.0, min(1.0, self.current_alert))

        # expose sub-organ values for viewer
        self.last_subvalues = subs

        return self.current_alert

    # ---------------- MASTER REGULATOR ----------------

    def _master_regulator(self, subs: Dict[str, float]):
        c = self.config

        weighted = {
            "threat_geometry": subs["threat_geometry"] * c.w_threat_geometry,
            "shadow_memory": subs["shadow_memory"] * c.w_shadow_memory,
            "storm_resonance": subs["storm_resonance"] * c.w_storm_resonance,
            "cognitive_load": subs["cognitive_load"] * c.w_cognitive_load,
            "shadow_drift": subs["shadow_drift"] * c.w_shadow_drift,
            "heartbeat_sync": subs["heartbeat_sync"] * c.w_heartbeat_sync,
            "meaning_collapse": subs["meaning_collapse"] * c.w_meaning_collapse,
            "chaos_gremlin": subs["chaos_gremlin"] * c.w_chaos_gremlin,
            "orientation_loss": subs["orientation_loss"] * c.w_orientation_loss,
            "emotional_volcano": subs["emotional_volcano"] * c.w_emotional_volcano,
        }

        spike_count = sum(1 for v in weighted.values() if v > 0.5)

        base_delta = sum(weighted.values()) / max(1, len(weighted))

        if spike_count >= c.spike_count_hard:
            delta = base_delta * 1.8
        elif spike_count >= c.spike_count_soft:
            delta = base_delta * 1.3
        else:
            delta = base_delta

        return delta, spike_count

    # ---------------- SUB-ORGANS ----------------

    def _get(self, metrics, key, default):
        v = metrics.get(key, default)
        try:
            return float(v)
        except:
            return default

    def _threat_geometry(self, metrics):
        drift = self._get(metrics, "drift", 0.0)
        storm = self._get(metrics, "storm", 0.0)
        sym = self._get(metrics, "symbolic_pressure", 0.0)
        stm_density = self._get(metrics, "stm_density", 0.0)

        values = [drift, storm, sym, stm_density]
        mean = sum(values) / 4.0
        var = sum((v - mean) ** 2 for v in values) / 4.0

        return min(1.0, var * 4.0)

    def _shadow_memory(self, metrics):
        unresolved_hooks = self._get(metrics, "unresolved_hooks", 0.0)
        unresolved_fragments = self._get(metrics, "unresolved_fragments", 0.0)
        abandoned_clusters = self._get(metrics, "abandoned_clusters", 0.0)

        raw = unresolved_hooks + unresolved_fragments + abandoned_clusters
        return max(0.0, min(1.0, raw / 10.0))

    def _storm_resonance(self, metrics):
        c = self.config
        storm = self._get(metrics, "storm", 0.0)
        drift = self._get(metrics, "drift", 0.0)

        if storm < 0.05:
            return 0.0

        if storm >= c.storm_high and drift >= c.drift_unstable:
            return min(1.0, storm * 1.5)
        elif storm >= c.storm_high:
            return storm * 0.4
        else:
            return storm * 0.7

    def _cognitive_load(self, metrics):
        c = self.config
        stm_word_count = self._get(metrics, "stm_word_count", 0.0)
        active_hooks = self._get(metrics, "active_hooks", 0.0)
        symbolic_packets = self._get(metrics, "symbolic_packets", 0.0)

        load = stm_word_count + active_hooks * 2.0 + symbolic_packets

        if stm_word_count <= c.stm_low and load < 3:
            return 0.5

        if stm_word_count >= c.stm_high or load > 60:
            return 1.0

        return 0.2

    def _shadow_drift(self, metrics):
        c = self.config
        drift = self._get(metrics, "drift", 0.0)
        prev_drift = self._get(metrics, "prev_drift", drift)
        drift_delta = drift - prev_drift

        prev_drift_delta = self._get(metrics, "prev_drift_delta", drift_delta)
        accel = drift_delta - prev_drift_delta

        magnitude = abs(accel)
        if magnitude < 0.05:
            return 0.0
        if magnitude >= c.drift_accel_high:
            return 1.0
        return magnitude / c.drift_accel_high

    def _heartbeat_sync(self, metrics):
        c = self.config
        heartbeat_tick = self._get(metrics, "heartbeat_tick", 0.0)
        viewer_tick = self._get(metrics, "viewer_tick", 0.0)

        diff = abs(heartbeat_tick - viewer_tick)

        if diff < 0.1:
            return 0.0
        if diff > 1.0:
            return min(1.0, diff * c.heartbeat_desync_penalty)
        return diff * (c.heartbeat_desync_penalty * 0.5)

    def _meaning_collapse(self, metrics):
        c = self.config
        sentence_comfort = self._get(metrics, "sentence_comfort", 1.0)
        symbolic_pressure = self._get(metrics, "symbolic_pressure", 1.0)
        word_strength = self._get(metrics, "word_strength", 1.0)
        concentration = self._get(metrics, "concentration", 1.0)

        low_count = 0
        if sentence_comfort < c.low_sentence_comfort:
            low_count += 1
        if symbolic_pressure < c.low_symbolic_pressure:
            low_count += 1
        if word_strength < c.low_word_strength:
            low_count += 1
        if concentration < c.low_concentration:
            low_count += 1

        if low_count == 0:
            return 0.0
        if low_count == 1:
            return 0.3
        if low_count == 2:
            return 0.6
        return 1.0

    def _chaos_gremlin(self, metrics):
        c = self.config
        chaos_force = self._get(metrics, "chaos_force", 0.0)
        gremlin_mischief = self._get(metrics, "gremlin_mischief", 0.0)
        gremlin_soothed = self._get(metrics, "gremlin_soothed", 0.0)

        raw = chaos_force + gremlin_mischief * 0.7 - gremlin_soothed * 0.8

        if raw <= 0:
            return 0.0
        if raw >= c.chaos_high:
            return 1.0
        return raw / c.chaos_high

    def _orientation_loss(self, metrics):
        has_goal = bool(metrics.get("active_goal", False))
        has_hook = bool(metrics.get("active_hook", False))
        has_story_thread = bool(metrics.get("active_story_thread", False))
        has_stm_cluster = bool(metrics.get("active_stm_cluster", False))

        missing = 0
        if not has_goal:
            missing += 1
        if not has_hook:
            missing += 1
        if not has_story_thread:
            missing += 1
        if not has_stm_cluster:
            missing += 1

        if missing == 0:
            return 0.0
        if missing == 1:
            return 0.3
        if missing == 2:
            return 0.6
        return 1.0

    def _emotional_volcano(self, metrics):
        c = self.config
        symbolic_pressure = self._get(metrics, "symbolic_pressure", 0.0)
        storm = self._get(metrics, "storm", 0.0)
        drift = self._get(metrics, "drift", 0.0)

        story_output_recent = bool(metrics.get("story_output_recent", False))
        movement_recent = bool(metrics.get("movement_recent", False))
        hook_chosen_recent = bool(metrics.get("hook_chosen_recent", False))

        high_pressure = (
            symbolic_pressure >= c.symbolic_pressure_high
            or storm >= c.storm_high
            or drift >= c.drift_unstable
        )

        no_outlet = not (story_output_recent or movement_recent or hook_chosen_recent)

        if high_pressure and no_outlet:
            return 1.0
        if high_pressure:
            return 0.4
        return 0.0
