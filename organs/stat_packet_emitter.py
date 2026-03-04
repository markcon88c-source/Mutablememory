# organs/stat_packet_emitter.py

class StatPacketEmitter:
    """
    Collects packets from the organism each cycle and emits
    a unified stats dict for downstream organs like the
    Emergence Viewer or EIX detector.

    This organ is the metabolic gland that converts packet-level
    signals into cycle-level statistics.
    """

    def __init__(self):
        # Nothing to store yet, but this organ may evolve later
        pass

    def build_stats(self, packets):
        """
        Convert raw packets into the stats dict required by the EIX detector.
        Each packet may contain:
          - weirdness
          - novelty
          - suffix_structure
          - drift
          - mutual_info
          - attractor_depth
          - entropy
          - emergence_raw

        Missing fields default to 0.0.
        """

        # Initialize accumulators
        acc = {
            "weirdness": 0.0,
            "novelty": 0.0,
            "suffix_structure": 0.0,
            "drift": 0.0,
            "mutual_info": 0.0,
            "attractor_depth": 0.0,
            "entropy": 0.0,
            "emergence_raw": 0.0,
        }

        n = max(len(packets), 1)

        # Sum all packet fields
        for p in packets:
            acc["weirdness"]         += p.get("weirdness", 0.0)
            acc["novelty"]           += p.get("novelty", 0.0)
            acc["suffix_structure"]  += p.get("suffix_structure", 0.0)
            acc["drift"]             += p.get("drift", 0.0)
            acc["mutual_info"]       += p.get("mutual_info", 0.0)
            acc["attractor_depth"]   += p.get("attractor_depth", 0.0)
            acc["entropy"]           += p.get("entropy", 0.0)
            acc["emergence_raw"]     += p.get("emergence_raw", 0.0)

        # Average across packets
        stats = {k: v / n for k, v in acc.items()}

        return stats
