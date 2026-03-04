class SparkModulationOrgan:
    """
    Computes spark_effective using:
      - raw spark
      - symbolic pressure
      - chaos
      - storm
      - stability
      - EIX (emergence index)

    Writes spark_effective into creature._last_meta["spark_effective"].
    """

    def __init__(self, creature):
        self.creature = creature

    def step(self):
        meta = getattr(self.creature, "_last_meta", {})

        # --- INPUTS ---
        raw_spark = meta.get("raw_spark", 0.0)
        symbolic = meta.get("symbolic", 0.0)
        chaos = meta.get("chaos", 0.0)
        storm = meta.get("storm", 0.0)
        stability = meta.get("stability", 0.5)
        eix = meta.get("eix", 0.0)

        # --- BASE SPARK ---
        # 0.15 floor + 0.45 raw spark + 0.40 instability
        base_spark = (
            0.15
            + 0.45 * raw_spark
            + 0.40 * (1 - stability)
        )

        # --- SUPPRESSION ---
        # symbolic is the primary spark killer
        suppression = (
            0.45 * symbolic +
            0.30 * chaos +
            0.25 * storm
        )

        # --- EIX BOOST ---
        # emergence increases ignition potential
        eix_boost = 0.35 * eix

        # --- FINAL SPARK ---
        spark_effective = base_spark - suppression + eix_boost
        spark_effective = max(0.0, min(1.0, spark_effective))

        # --- WRITE BACK ---
        meta["spark_effective"] = spark_effective
        self.creature._last_meta = meta

        return spark_effective
