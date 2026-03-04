class IntegrityViewer:
    """
    Diagnostic viewer that confirms:
      • packet integrity
      • force completeness
      • pressure completeness
      • STM metrics
      • drift + pressure summaries
    """

    def __init__(self, creature):
        self.creature = creature

    def render(self, packet=None):
        # ---------------------------------------------------------
        # UNWRAP LIST FROM ORCHESTRATOR
        # ---------------------------------------------------------
        if isinstance(packet, list):
            packet = packet[0] if packet else None

        lines = []
        lines.append("=" * 60)
        lines.append("🧠 STM INTEGRITY VIEWER")
        lines.append("=" * 60)

        # ---------------------------------------------------------
        # PACKET INTEGRITY
        # ---------------------------------------------------------
        if packet is None:
            lines.append("")
            lines.append("(no packet provided)")
        else:
            lines.append("")
            lines.append("📦 PACKET INTEGRITY")
            lines.append("-" * 60)
            lines.append(f"Word: {packet.get('word')}")
            lines.append(f"Forces OK: {'forces' in packet}")
            lines.append(f"Pressures OK: {'pressures' in packet}")
            lines.append(f"Metrics OK: {'metrics' in packet}")

        # ---------------------------------------------------------
        # STM METRICS
        # ---------------------------------------------------------
        stm = self.creature.stm.get_metrics()
        lines.append("")
        lines.append("🧩 STM METRICS")
        lines.append("-" * 60)
        lines.append(f"Word Count: {stm['word_count']}")
        lines.append(f"Density: {stm['density']:.3f}")
        lines.append(f"Unresolved Hooks: {stm['unresolved_hooks']}")
        lines.append(f"Unresolved Fragments: {stm['unresolved_fragments']}")
        lines.append(f"Abandoned Clusters: {stm['abandoned_clusters']}")

        # ---------------------------------------------------------
        # DRIFT SUMMARY
        # ---------------------------------------------------------
        drift = stm["drift_summary"]
        lines.append("")
        lines.append("🌬️ DRIFT SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Average Drift: {drift['avg']:.3f}")
        lines.append(f"Last Drift: {drift['last']:.3f}")

        # ---------------------------------------------------------
        # PRESSURE SUMMARY
        # ---------------------------------------------------------
        ps = stm["pressure_summary"]
        lines.append("")
        lines.append("⚡ PRESSURE SUMMARY")
        lines.append("-" * 60)
        lines.append("Average Pressures:")
        for k, v in ps["avg"].items():
            lines.append(f"  {k}: {v:.3f}")

        lines.append("")
        lines.append("Last Pressure Snapshot:")
        for k, v in ps["last"].items():
            lines.append(f"  {k}: {v:.3f}")

        lines.append("=" * 60)
        return lines
