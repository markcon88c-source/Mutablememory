# packet_source_adaptor.py
# 🧬 PacketSourceAdaptor
# Wraps any organ and extracts packets safely.

class PacketSourceAdaptor:
    """
    Universal packet adaptor.
    Attach to ANY organ and it will:
      - detect if the organ produces packets
      - call build_packets() if available
      - read last_packets if available
      - normalize dict/float/list
      - return a clean packet list
    """

    def __init__(self, organ):
        self.organ = organ

    def get_packets(self):
        packets = []

        # 1. If organ has build_packets(), call it
        if hasattr(self.organ, "build_packets"):
            try:
                raw = self.organ.build_packets()
                packets.extend(self._normalize(raw))
            except Exception:
                pass  # immune system: ignore malformed packets

        # 2. If organ has last_packets, read them
        if hasattr(self.organ, "last_packets"):
            try:
                raw = self.organ.last_packets
                packets.extend(self._normalize(raw))
            except Exception:
                pass

        return packets

    def _normalize(self, raw):
        """
        Normalize raw packet output:
        - None → []
        - dict → [dict]
        - float/int → [{"type": "value", "value": raw}]
        - list → list
        """
        if raw is None:
            return []

        if isinstance(raw, dict):
            # ensure packet type
            if "type" not in raw:
                raw["type"] = "unknown"
            return [raw]

        if isinstance(raw, (float, int)):
            return [{"type": "value", "value": float(raw)}]

        if isinstance(raw, list):
            normalized = []
            for p in raw:
                if isinstance(p, dict):
                    if "type" not in p:
                        p["type"] = "unknown"
                    normalized.append(p)
                else:
                    normalized.append({"type": "value", "value": p})
            return normalized

        # fallback
        return [{"type": "unknown", "value": raw}]
