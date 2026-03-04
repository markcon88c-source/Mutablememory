# universal_adaptor.py
# 🫀 UniversalAdaptor — runs organ.step() safely every heartbeat

class UniversalAdaptor:
    def __init__(self, organ):
        self.organ = organ

    def heartbeat(self):
        """
        Safely call organ.step() every heartbeat.
        """
        try:
            self.organ.step()
        except Exception as e:
            print("UniversalAdaptor caught error:", e)
