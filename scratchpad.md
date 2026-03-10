            "kind": "tick",
            "payload": {}
        })

        # 2) Tick all organs
        for organ in self.registry.values():
            try:
                organ.tick()
            except Exception as e:
                print("[BUS] organ tick error:", e)
